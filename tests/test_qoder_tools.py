from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import re
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "ux-decision-advisor"
SCRIPTS = SKILL / "scripts"
sys.path.insert(0, str(SCRIPTS))

import analyze_synthetic  # noqa: E402
import local_evidence  # noqa: E402
import package_skill  # noqa: E402
import render_markdown_report  # noqa: E402
import render_report  # noqa: E402
import validate_evidence  # noqa: E402
import validate_skill  # noqa: E402


class SkillValidationTests(unittest.TestCase):
    def test_candidate_contract(self):
        result = validate_skill.validate(SKILL)
        self.assertEqual(result["name"], "ux-decision-advisor")
        self.assertGreaterEqual(result["references"], 70)
        self.assertLessEqual(result["skill_body_lines"], 500)
        self.assertGreaterEqual(result["scripts"], 20)
        self.assertIn('version: "0.1.0-beta.5-integration.1"', (SKILL / "SKILL.md").read_text(encoding="utf-8"))

    def test_layered_output_contract_is_present(self):
        entry = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        output = (SKILL / "references" / "decision-and-business-output.md").read_text(encoding="utf-8")
        self.assertIn("Direct answer", entry)
        self.assertIn("Optional explanation", entry)
        self.assertIn("Executable artifact", entry)
        self.assertIn("Optional detail: method / protocol / evidence audit", output)

    def test_qualitative_slice_is_operational(self):
        analysis = (SKILL / "references" / "analysis-and-statistics.md").read_text(encoding="utf-8")
        worksheet = (SKILL / "assets" / "qualitative-coding.md").read_text(encoding="utf-8")
        for term in ("codebook_version", "double-code", "adjudicate", "negative cases", "saturation"):
            self.assertIn(term, analysis.lower())
        self.assertIn("Contradicting independent sources", worksheet)

    def test_broken_link_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            skill = Path(tmp) / "ux-decision-advisor"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: ux-decision-advisor\ndescription: Test skill\n---\n\n# Qoder Local Pilot\n[Missing](references/missing.md)\n",
                encoding="utf-8",
            )
            with self.assertRaises(validate_skill.ValidationIssue):
                validate_skill.validate(skill)


class EvidenceContractTests(unittest.TestCase):
    def payload(self):
        return json.loads((SKILL / "assets" / "uxda-evidence-example.json").read_text(encoding="utf-8"))

    def test_example_record_is_valid_without_truth_claim(self):
        result = validate_evidence.validate(self.payload())
        self.assertEqual(result["reference_checks"], "passed")
        self.assertEqual(result["truth_verification"], "not_performed")
        self.assertTrue(result["synthetic"])

    def test_broken_evidence_reference_is_rejected(self):
        payload = self.payload()
        payload["claims"][0]["evidence_refs"] = ["E-MISSING"]
        with self.assertRaises(validate_evidence.EvidenceIssue) as caught:
            validate_evidence.validate(payload)
        self.assertIn("BROKEN_CLAIM_EVIDENCE_REFERENCE", str(caught.exception))

    def test_unauthorized_evidence_is_rejected(self):
        payload = self.payload()
        payload["evidence"][0]["authorized_for_use"] = False
        with self.assertRaises(validate_evidence.EvidenceIssue) as caught:
            validate_evidence.validate(payload)
        self.assertIn("EVIDENCE_NOT_AUTHORIZED", str(caught.exception))

    def test_undefined_confidence_field_is_rejected(self):
        payload = self.payload()
        payload["claims"][0]["confidence"] = 0.8
        with self.assertRaises(validate_evidence.EvidenceIssue) as caught:
            validate_evidence.validate(payload)
        self.assertIn("UNDEFINED_CONFIDENCE_FIELD", str(caught.exception))

    def test_supported_claim_requires_evidence(self):
        payload = self.payload()
        payload["claims"][0]["status"] = "supported"
        payload["claims"][0]["evidence_refs"] = []
        with self.assertRaises(validate_evidence.EvidenceIssue) as caught:
            validate_evidence.validate(payload)
        self.assertIn("SUPPORTED_CLAIM_REQUIRES_EVIDENCE", str(caught.exception))

    def test_invalid_enum_type_fails_cleanly(self):
        payload = self.payload()
        payload["studies"][0]["method"] = []
        with self.assertRaises(validate_evidence.EvidenceIssue) as caught:
            validate_evidence.validate(payload)
        self.assertIn("ENUM_INVALID", str(caught.exception))

    def test_cross_study_evidence_reference_is_rejected(self):
        payload = self.payload()
        second_study = dict(payload["studies"][0])
        second_study["study_id"] = "S-002"
        payload["studies"].append(second_study)
        payload["evidence"][1]["study_id"] = "S-002"
        payload["claims"][0]["evidence_refs"] = ["E-002"]
        payload["claims"][1]["evidence_refs"] = ["E-001"]
        with self.assertRaises(validate_evidence.EvidenceIssue) as caught:
            validate_evidence.validate(payload)
        self.assertIn("CROSS_STUDY_CLAIM_EVIDENCE_REFERENCE", str(caught.exception))

    def test_non_extended_date_is_rejected(self):
        payload = self.payload()
        payload["decisions"][0]["review_date"] = "20261201"
        with self.assertRaises(validate_evidence.EvidenceIssue) as caught:
            validate_evidence.validate(payload)
        self.assertIn("DATE_INVALID", str(caught.exception))

    def test_schema_mirrors_runtime_guards(self):
        schema = json.loads((SKILL / "assets" / "uxda-evidence-v1.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["$defs"]["evidence"]["properties"]["authorized_for_use"]["const"], True)
        self.assertIn("allOf", schema["$defs"]["claim"])
        self.assertIn("allOf", schema["$defs"]["decision"])
        self.assertIn("pattern", schema["$defs"]["decision"]["properties"]["review_date"])

    def test_invalid_utf8_fails_cleanly(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            path = Path(tmp) / "invalid.json"
            path.write_bytes(b"\xff\xfe")
            with self.assertRaises(validate_evidence.EvidenceIssue) as caught:
                validate_evidence.load(path)
            self.assertIn("INVALID_JSON", str(caught.exception))

    def test_duplicate_json_key_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            path = Path(tmp) / "duplicate.json"
            path.write_text('{"schema_version":"uxda-evidence-v1","schema_version":"uxda-evidence-v1"}', encoding="utf-8")
            with self.assertRaises(validate_evidence.EvidenceIssue) as caught:
                validate_evidence.load(path)
            self.assertIn("DUPLICATE_JSON_KEY", str(caught.exception))


class SyntheticAnalysisTests(unittest.TestCase):
    def test_failures_missing_outliers_and_pairs(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            output = Path(tmp) / "analysis.json"
            result = analyze_synthetic.run(
                ROOT / "tests" / "data" / "synthetic_task_times.csv",
                output,
                ROOT / "tests" / "data" / "synthetic_config.json",
                None,
                None,
            )
            self.assertTrue(result["synthetic"])
            self.assertEqual(result["row_count"], 10)
            group_a = next(g for g in result["groups"] if g["condition"] == "A")
            self.assertEqual(group_a["n_records"], 5)
            self.assertEqual(group_a["n_success"], 3)
            self.assertEqual(group_a["n_failure"], 1)
            self.assertEqual(group_a["n_missing_success"], 1)
            self.assertEqual(group_a["n_missing_duration"], 1)
            self.assertEqual(group_a["success_rate_pct_bounds_all_records"]["missing_as_failure"], 60.0)
            self.assertEqual(group_a["success_rate_pct_bounds_all_records"]["missing_as_success"], 80.0)
            self.assertIn(8, group_a["tukey_outlier_row_numbers"])
            success_pairs = result["paired_success"][0]
            self.assertEqual(success_pairs["n_complete_outcome_pairs"], 4)
            self.assertEqual(success_pairs["a_success_pct_within_complete_pairs"], 75.0)
            self.assertEqual(success_pairs["b_success_pct_within_complete_pairs"], 75.0)
            self.assertEqual(group_a["duration_all_observed_excluding_flagged"]["mean"], 12.0)
            paired = result["paired_differences"][0]
            self.assertEqual(paired["n_complete_duration_pairs"], 4)
            self.assertEqual(paired["median_b_minus_a"], 2.0)
            self.assertEqual(paired["mean_b_minus_a"], -17.5)
            paired_sensitivity = result["paired_differences_excluding_flagged_rows"][0]
            self.assertEqual(paired_sensitivity["n_complete_duration_pairs"], 3)
            self.assertEqual(paired_sensitivity["mean_b_minus_a"], 4.0)
            self.assertNotIn("median_b_minus_a_seconds", paired)
            self.assertTrue(output.is_file())

    def test_duplicate_key_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            path = Path(tmp) / "duplicate.csv"
            path.write_text(
                "participant_id,condition,task,success,duration_seconds\nP1,A,T,1,10\nP1,A,T,1,11\n",
                encoding="utf-8",
            )
            with self.assertRaises(analyze_synthetic.InputIssue):
                analyze_synthetic.read_rows(path)

    def test_invalid_success_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            path = Path(tmp) / "invalid.csv"
            path.write_text(
                "participant_id,condition,task,success,duration_seconds\nP1,A,T,maybe,10\n",
                encoding="utf-8",
            )
            with self.assertRaises(analyze_synthetic.InputIssue):
                analyze_synthetic.read_rows(path)

    def test_output_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            path = Path(tmp) / "input.csv"
            original = "participant_id,condition,task,success,duration_seconds\nP1,A,T,1,10\n"
            path.write_text(original, encoding="utf-8")
            with self.assertRaises(analyze_synthetic.InputIssue):
                analyze_synthetic.run(path, path, None, True, None)
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_output_cannot_overwrite_config(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            folder = Path(tmp)
            source = folder / "input.csv"
            source.write_text(
                "participant_id,condition,task,success,duration_seconds\nP1,A,T,1,10\n",
                encoding="utf-8",
            )
            config = folder / "config.json"
            original = json.dumps({"synthetic": True})
            config.write_text(original, encoding="utf-8")
            with self.assertRaises(analyze_synthetic.InputIssue):
                analyze_synthetic.run(source, config, config, None, None)
            self.assertEqual(config.read_text(encoding="utf-8"), original)

    def test_non_second_unit_is_rejected_for_seconds_column(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            folder = Path(tmp)
            source = folder / "input.csv"
            source.write_text(
                "participant_id,condition,task,success,duration_seconds\nP1,A,T,1,10\nP1,B,T,1,12\n",
                encoding="utf-8",
            )
            config = folder / "config.json"
            config.write_text(json.dumps({"synthetic": True, "duration_unit": "minutes"}), encoding="utf-8")
            with self.assertRaises(analyze_synthetic.InputIssue) as caught:
                analyze_synthetic.run(source, folder / "out.json", config, None, None)
            self.assertEqual(str(caught.exception), "DURATION_COLUMN_UNIT_MISMATCH")


class ReportTests(unittest.TestCase):
    def payload(self):
        return {
            "title": "Synthetic <script>alert(1)</script> demo",
            "summary": "Synthetic demonstration only.",
            "recommendation": "Do not infer a product effect.",
            "next_step": "Verify with an authorized study.",
            "evidence_boundary": "Synthetic data only; no real product effect.",
            "language": "en",
            "synthetic": True,
            "sections": [{"heading": "Question", "body": "Can the analysis reproduce counts?"}],
        }

    def test_safe_rendering(self):
        payload = render_report.validate(self.payload())
        html = render_report.render(payload)
        self.assertIn("\\u003cscript\\u003ealert", html)
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("Synthetic demonstration", html)

    def test_url_requires_inspection_record(self):
        payload = self.payload()
        payload["evidence"] = [{"title": "Source", "note": "Claim", "url": "https://example.com/source"}]
        with self.assertRaises(render_report.InputIssue):
            render_report.validate(payload)

    def test_metric_requires_denominator(self):
        payload = self.payload()
        payload["metrics"] = [{"label": "Success", "n": 5, "value": 60, "unit": "%"}]
        with self.assertRaises(render_report.InputIssue):
            render_report.validate(payload)

    def test_hardlink_output_is_rejected(self):
        import os
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            path = Path(tmp) / "report.json"
            original = json.dumps(self.payload())
            path.write_text(original, encoding="utf-8")
            output = Path(tmp) / "hardlink.html"
            os.link(path, output)
            argv = ["render_report.py", "--input", str(path), "--output", str(output)]
            with mock.patch.object(sys, "argv", argv), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(render_report.main(), 2)
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_output_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            path = Path(tmp) / "report.json"
            original = json.dumps(self.payload())
            path.write_text(original, encoding="utf-8")
            argv = ["render_report.py", "--input", str(path), "--output", str(path)]
            with mock.patch.object(sys, "argv", argv), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(render_report.main(), 2)
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_hidden_sections_have_css(self):
        shell = (SKILL / "assets" / "report-shell.html").read_text(encoding="utf-8")
        self.assertIn(".hidden{display:none!important}", shell)

    def test_bilingual_labels_and_source_metadata_are_rendered(self):
        shell = (SKILL / "assets" / "structured-report-shell.html").read_text(encoding="utf-8")
        self.assertIn("const t = (en, cn)", shell)
        self.assertIn("当前判断", shell)
        self.assertIn("support_excerpt", shell)
        self.assertIn("source_retrieval_ref", shell)


class MarkdownReportTests(unittest.TestCase):
    def test_inline_escaping_and_safe_links(self):
        rendered = render_markdown_report.inline_markdown('<script>alert(1)</script> **结论** [来源](https://example.com)')
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertIn("<strong>结论</strong>", rendered)
        self.assertIn('href="https://example.com"', rendered)

    def test_table_rendering(self):
        markdown = "| 假设 | 状态 |\n|---|---|\n| 入口未被注意 | 待验证 |\n"
        rendered = render_markdown_report.markdown_to_html(markdown)
        self.assertIn("<table>", rendered)
        self.assertIn('<th scope="col">假设</th>', rendered)
        self.assertIn("<td>待验证</td>", rendered)

    def test_headings_lists_and_code(self):
        markdown = "# 标题\n\n- 第一项\n- 第二项\n\n```python\nprint('ok')\n```\n"
        rendered = render_markdown_report.markdown_to_html(markdown)
        self.assertIn("<h1>标题</h1>", rendered)
        self.assertIn("<ul>", rendered)
        self.assertIn("language-python", rendered)

    def test_mermaid_flowchart_renders_svg(self):
        source = "flowchart TD\nA[业务现象] --> B[研究问题]\nB --> C{证据是否足够}\n"
        rendered = render_markdown_report.render_mermaid(source)
        self.assertIn('<svg class="mermaid-svg"', rendered)
        self.assertIn("业务现象", rendered)
        self.assertIn("<polygon", rendered)

    def test_unsupported_mermaid_has_readable_fallback(self):
        rendered = render_markdown_report.render_mermaid("sequenceDiagram\nAlice->>Bob: Hello")
        self.assertIn("diagram fallback", rendered)
        self.assertIn("sequenceDiagram", rendered)
        self.assertNotIn("<svg", rendered)

    def test_raw_html_and_remote_images_are_not_executed(self):
        markdown = '<img src=x onerror=alert(1)>\n\n![远程图](https://example.com/image.png)'
        rendered = render_markdown_report.markdown_to_html(markdown)
        self.assertNotIn("<img src=x", rendered)
        self.assertIn("外部图片未嵌入", rendered)
        self.assertNotIn('src="https://example.com/image.png"', rendered)

    def test_frontmatter_and_language_detection(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            folder = Path(tmp)
            source = folder / "report.md"
            source.write_text("---\ntitle: 中文报告\nlanguage: zh\n---\n# 正文\n\n内容。\n", encoding="utf-8")
            metadata, body = render_markdown_report.read_markdown(source)
            self.assertEqual(metadata["title"], "中文报告")
            self.assertEqual(render_markdown_report.detect_language(body), "zh")
            result = render_markdown_report.run(source, folder / "report.html")
            self.assertEqual(result["language"], "zh")
            page = (folder / "report.html").read_text(encoding="utf-8")
            self.assertIn('<html lang="zh-CN">', page)
            self.assertIn("中文报告", page)

    def test_output_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            path = Path(tmp) / "report.md"
            original = "# 标题\n\n正文。\n"
            path.write_text(original, encoding="utf-8")
            argv = ["render_markdown_report.py", "--input", str(path), "--output", str(path)]
            with mock.patch.object(sys, "argv", argv), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(render_markdown_report.main(), 2)
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_mermaid_chain_and_complex_label(self):
        source = "flowchart TD\nA[开始] --> B[处理] --> C[结束]\nA[检查 test(ok)] --> D[完成]\n"
        parsed = render_markdown_report.parse_mermaid(source)
        self.assertIsNotNone(parsed)
        self.assertEqual(len(parsed[3]), 3)
        self.assertNotIn("test", parsed[1])
        self.assertEqual(parsed[1]["A"], "检查 test(ok)")

    def test_mermaid_trailing_syntax_falls_back(self):
        rendered = render_markdown_report.render_mermaid("flowchart TD\nA --> B;")
        self.assertIn("diagram fallback", rendered)

    def test_long_chinese_label_wraps(self):
        lines = render_markdown_report.wrap_label("这是一个需要换行显示的中文长标签用于验证节点宽度")
        self.assertGreater(len(lines), 1)
        self.assertTrue(all(render_markdown_report.display_width(line) <= 24 for line in lines))

    def test_english_interface_is_localized(self):
        page = render_markdown_report.render_page("Title", "", "en", "<p>Body</p>", "# Source")
        self.assertIn("Print / Save PDF", page)
        self.assertIn("View source Markdown", page)
        self.assertNotIn("查看原始 Markdown", page)

    def test_hardlink_output_is_rejected(self):
        import os
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            folder = Path(tmp)
            source = folder / "report.md"
            original = "# 标题\n\n正文。\n"
            source.write_text(original, encoding="utf-8")
            output = folder / "hardlink.html"
            os.link(source, output)
            with self.assertRaises(render_markdown_report.InputIssue):
                render_markdown_report.run(source, output)
            self.assertEqual(source.read_text(encoding="utf-8"), original)

    def test_skill_tree_output_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            source = Path(tmp) / "report.md"
            source.write_text("# 标题\n", encoding="utf-8")
            with self.assertRaises(render_markdown_report.InputIssue):
                render_markdown_report.run(source, SKILL / "should-not-exist.html")

    def test_multiple_mermaid_marker_ids_are_unique(self):
        first = render_markdown_report.render_mermaid("flowchart TD\nA --> B")
        second = render_markdown_report.render_mermaid("flowchart TD\nC --> D")
        first_id = re.search(r'marker id="([^"]+)"', first).group(1)
        second_id = re.search(r'marker id="([^"]+)"', second).group(1)
        self.assertNotEqual(first_id, second_id)

    def test_chinese_mermaid_integration_keeps_chinese_ui(self):
        markdown = "# 标题\n\n```mermaid\nflowchart TD\nA[开始] --> B[结束]\n```\n"
        rendered = render_markdown_report.markdown_to_html(markdown, "zh")
        self.assertIn("Markdown Mermaid 流程图", rendered)
        self.assertIn('aria-label="Markdown Mermaid 流程图"', rendered)
        self.assertNotIn("Markdown Mermaid flowchart", rendered)

    def test_english_remote_image_and_disabled_link_messages(self):
        rendered = render_markdown_report.inline_markdown(
            '![remote](https://example.com/image.png) [bad](javascript:alert(1))', "en"
        )
        self.assertIn("External image not embedded", rendered)
        self.assertIn("Link disabled", rendered)
        self.assertNotIn("外部图片未嵌入", rendered)
        self.assertNotIn("链接未启用", rendered)

    def test_page_title_is_escaped(self):
        page = render_markdown_report.render_page("<script>alert(1)</script>", "", "zh", "<p>正文</p>", "# 源")
        self.assertNotIn("<title><script>", page)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", page)


class PackagingTests(unittest.TestCase):
    def make_source(self, root: Path) -> Path:
        source = root / "ux-decision-advisor"
        source.mkdir()
        files = {
            "SKILL.md": "---\nname: ux-decision-advisor\ndescription: Test\n---\n# Qoder Local Pilot\n",
            "LICENSE": "License\n",
            "assets/markdown-report-shell.html": "<html>__TITLE__</html>\n",
            "assets/report-shell.html": "<html>__JSON_DATA__</html>\n",
            "scripts/render_markdown_report.py": "pass\n",
            "scripts/render_report.py": "pass\n",
            "scripts/validate_evidence.py": "pass\n",
            "scripts/analyze_synthetic.py": "pass\n",
            "scripts/local_evidence.py": "pass\n",
            "assets/structured-report-shell.html": "<html></html>\n",
            "assets/uxda-evidence-v1.schema.json": "{}\n",
            "assets/uxda-evidence-example.json": "{}\n",
            "assets/qualitative-coding.md": "# Coding\n",
            "references/core-reasoning.md": "# Core\n",
            "references/business-facing-output-contract.md": "# Contract\n",
            "references/bilingual-parity.md": "# Parity\n",
            "run.py": "print('ok')\n",
        }
        for relative, content in files.items():
            path = source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        return source

    def test_zip_layout_and_digest(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            source = self.make_source(Path(tmp))
            output = Path(tmp) / "skill.zip"
            result = package_skill.build(source, output)
            self.assertEqual(result["file_count"], 17)
            self.assertEqual(result["sha256"], hashlib.sha256(output.read_bytes()).hexdigest())
            with zipfile.ZipFile(output) as archive:
                self.assertEqual(len(archive.namelist()), 17)
                self.assertIn("ux-decision-advisor/assets/markdown-report-shell.html", archive.namelist())
                self.assertIsNone(archive.testzip())

    def test_manifest_cannot_enter_source(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            source = self.make_source(Path(tmp))
            with self.assertRaises(package_skill.PackageIssue):
                package_skill.build(source, Path(tmp) / "skill.zip", source / "manifest.json")

    def test_manifest_cannot_overwrite_zip(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            source = self.make_source(Path(tmp))
            output = Path(tmp) / "skill.zip"
            with self.assertRaises(package_skill.PackageIssue):
                package_skill.build(source, output, output)
            self.assertFalse(output.exists())

    def test_missing_runtime_dependency_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            source = self.make_source(Path(tmp))
            (source / "assets/markdown-report-shell.html").unlink()
            with self.assertRaises(package_skill.PackageIssue) as caught:
                package_skill.build(source, Path(tmp) / "skill.zip")
            self.assertIn("REQUIRED_RUNTIME_MISSING", str(caught.exception))


class LocalEvidenceTests(unittest.TestCase):
    def test_exact_term_retrieval(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as tmp:
            folder = Path(tmp)
            doc = folder / "voc.md"
            doc.write_text("# VOC\nUser reported network instability during export.\n", encoding="utf-8")
            manifest = folder / "manifest.json"
            manifest.write_text(json.dumps({"sources": [{"id": "voc", "role": "voc", "path": str(doc)}]}), encoding="utf-8")
            output = folder / "pack.json"
            result = local_evidence.run(manifest, ["network"], output, limit=10, include_excerpts=False)
            self.assertEqual(result["total_matching_units"], 1)
            self.assertEqual(result["matches"][0]["source_id"], "voc")
            self.assertNotIn("excerpt", result["matches"][0])
            self.assertTrue(output.is_file())

    def test_source_repo_is_protected(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as tmp:
            folder = Path(tmp)
            doc = folder / "voc.md"
            doc.write_text("network\n", encoding="utf-8")
            manifest = folder / "manifest.json"
            manifest.write_text(json.dumps({"sources": [{"id": "voc", "role": "voc", "path": str(doc)}]}), encoding="utf-8")
            with self.assertRaises(local_evidence.InputIssue) as caught:
                local_evidence.run(manifest, ["network"], folder / "pack.json")
            self.assertEqual(str(caught.exception), "PUBLIC_TREE_BOUNDARY")

    def test_output_cannot_overwrite_decision_record(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as tmp:
            folder = Path(tmp)
            doc = folder / "voc.md"
            doc.write_text("network instability\n", encoding="utf-8")
            manifest = folder / "manifest.json"
            manifest.write_text(json.dumps({"sources": [{"id": "voc", "role": "voc", "path": str(doc)}]}), encoding="utf-8")
            previous = folder / "previous.json"
            local_evidence.run(manifest, ["network"], previous)
            decision = folder / "decision.json"
            decision.write_text(json.dumps({"claims": []}), encoding="utf-8")
            with self.assertRaises(local_evidence.InputIssue) as caught:
                local_evidence.run(manifest, ["network"], decision, previous=previous, decision_record=decision)
            self.assertEqual(str(caught.exception), "OUTPUT_OVERWRITES_DECISION_RECORD")

    def test_json_keys_and_csv_headers_are_searchable(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as tmp:
            folder = Path(tmp)
            json_doc = folder / "data.json"
            json_doc.write_text(json.dumps({"network_issue": "ok"}), encoding="utf-8")
            csv_doc = folder / "data.csv"
            csv_doc.write_text("network,value\nx,1\n", encoding="utf-8")
            manifest = folder / "manifest.json"
            manifest.write_text(json.dumps({"sources": [
                {"id": "json", "role": "other", "path": str(json_doc)},
                {"id": "csv", "role": "other", "path": str(csv_doc)},
            ]}), encoding="utf-8")
            result = local_evidence.run(manifest, ["network"], folder / "pack.json")
            self.assertEqual(result["total_matching_units"], 2)
            self.assertEqual({m["source_id"] for m in result["matches"]}, {"json", "csv"})


if __name__ == "__main__":
    unittest.main()
