import copy
import importlib.util
from pathlib import Path
import unittest

script=Path(__file__).resolve().parents[1]/"skills/korean-job-discovery/scripts/discovery.py"
spec=importlib.util.spec_from_file_location("discovery",script)
d=importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)

class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.catalog=d.load_catalog()
    def plan(self,**kwargs):
        return d.plan(self.catalog,["it"],research_date="2026-10-06",**kwargs)
    def completed(self):
        run=self.plan()
        for r in run["routes"]:
            if r["selected"]:
                r.update(status="checked",checked_at="2026-10-06T08:00:00+09:00",
                         scope_or_query="SYNTHETIC TEST ONLY",
                         evidence_url="https://example.invalid/test",
                         evidence_level="body",evidence_note="SYNTHETIC TEST ONLY",
                         discovered_count=0)
        return run
    def test_catalog_integrity(self):
        self.assertEqual(d.catalog_errors(self.catalog),[])
        self.assertTrue({"office","accounting","sales","marketing","design","media",
                         "healthcare","welfare","education","retail","hospitality",
                         "manufacturing","logistics","trades","part_time"}
                        <= set(self.catalog["track_presets"]))
    def test_default_is_general_unrestricted_experience(self):
        run=d.plan(self.catalog,research_date="2026-10-06")
        self.assertEqual(run["request"]["tracks"],["general"])
        self.assertEqual(run["request"]["level"],"any")
        self.assertEqual(run["request"]["audiences"],[])
        selected={r["route_id"] for r in run["routes"] if r["selected"]}
        self.assertTrue(set(self.catalog["baseline_ids"]) <= selected)
        self.assertFalse({"jumpit","rndjob","aw","thevc","rnjob","saeil"} & selected)
    def test_nontechnical_tracks_do_not_force_technical_rosters(self):
        for track in ["office","marketing","design","healthcare","education","retail",
                      "hospitality","manufacturing","logistics","part_time"]:
            run=d.plan(self.catalog,[track],research_date="2026-10-06")
            selected={r["route_id"] for r in run["routes"] if r["selected"]}
            self.assertFalse({"aw","thevc","rndjob","jumpit"} & selected,track)
            self.assertIn("greeting",selected)
    def test_specialist_duties_choose_their_boards(self):
        expected={"accounting":"semoojob","marketing":"iboss","design":"designerjob",
                  "media":"mediajob","retail":"shopma","hospitality":"foodnjob",
                  "education":"hunjang","healthcare":"medijob","trades":"construction-worknet"}
        for track, ident in expected.items():
            selected={r["route_id"] for r in d.plan(self.catalog,[track])["routes"] if r["selected"]}
            self.assertIn(ident,selected,track)
    def test_audience_routes_are_explicit_supplements(self):
        targeted={ident for ids in self.catalog["audience_presets"].values() for ident in ids}
        for tracks in [["general"],["office"],["welfare"],["part_time"]]:
            selected={r["route_id"] for r in d.plan(self.catalog,tracks)["routes"] if r["selected"]}
            self.assertFalse(targeted & selected)
        selected={r["route_id"] for r in d.plan(self.catalog,["office"],audiences=["midcareer"])["routes"] if r["selected"]}
        self.assertIn("midcareer-center",selected)
        self.assertIn("saramin",selected)
        self.assertNotIn("saeil",selected)
    def test_unknown_audience_rejected(self):
        with self.assertRaises(ValueError):
            d.plan(self.catalog,audiences=["guessed-group"])
    def test_experienced_office_prioritizes_experienced_board(self):
        selected={r["route_id"] for r in d.plan(self.catalog,["office"],level="experienced")["routes"] if r["selected"]}
        self.assertIn("businesspeople",selected)
        self.assertNotIn("inthiswork",selected)
    def test_local_part_time_board_in_initial_plan(self):
        selected={r["route_id"] for r in d.plan(self.catalog,["hospitality","part_time"],region="인천")["routes"] if r["selected"]}
        self.assertIn("daangn-jobs",selected)
    def test_education_region_seed_requires_region_and_track(self):
        for tracks,region,expected in [(["education"],"경기도",True),
                                      (["education"],"서울",False),(["office"],"경기도",False)]:
            selected={r["route_id"] for r in d.plan(self.catalog,tracks,region=region)["routes"] if r["selected"]}
            self.assertEqual("gyeonggi-education" in selected,expected)
    def test_general_region_does_not_force_industrial_directory(self):
        selected={r["route_id"] for r in d.plan(self.catalog,region="부산")["routes"] if r["selected"]}
        self.assertIn("busan-company",selected)
        self.assertNotIn("busan-industrial-park",selected)
        self.assertNotIn("changwon-department",selected)
    def test_catalog_rejects_dangling_optional_presets(self):
        for key in ["directory_presets","audience_presets"]:
            catalog=copy.deepcopy(self.catalog)
            catalog[key]["office"]=["missing-route"]
            self.assertTrue(d.catalog_errors(catalog))
    def test_plan_does_not_inherit_seed_checks(self):
        self.assertTrue(all(r["status"]=="unverified" and r["checked_at"] is None
                            for r in self.plan()["routes"]))
    def test_directory_and_ats_in_broad(self):
        selected={r["route_id"] for r in self.plan()["routes"] if r["selected"]}
        self.assertTrue({"thevc","greeting"} <= selected)
    def test_company_focus_excludes_rosters(self):
        run=self.plan(mode="company",company="Example",region="부산")
        selected={r["route_id"] for r in run["routes"] if r["selected"]}
        self.assertNotIn("thevc",selected)
        self.assertNotIn("busan-industrial-park",selected)
    def test_company_name_required(self):
        with self.assertRaises(ValueError):
            self.plan(mode="company")
    def test_public_only_does_not_force_startup_directory(self):
        run=d.plan(self.catalog,["public"],research_date="2026-10-06")
        selected={r["route_id"] for r in run["routes"] if r["selected"]}
        self.assertNotIn("thevc",selected)
    def test_rnd_uses_industry_roster(self):
        run=d.plan(self.catalog,["rnd"],research_date="2026-10-06")
        selected={r["route_id"] for r in run["routes"] if r["selected"]}
        self.assertIn("aw",selected)
    def test_unknown_track_rejected(self):
        with self.assertRaises(ValueError):
            d.plan(self.catalog,["made-up"])
    def test_region_does_not_force_busan_on_seoul(self):
        selected={r["route_id"] for r in self.plan(region="서울")["routes"] if r["selected"]}
        self.assertNotIn("pusan-university",selected)
    def test_busan_sources_selected(self):
        selected={r["route_id"] for r in self.plan(region="Busan")["routes"] if r["selected"]}
        self.assertIn("pusan-university",selected)
    def test_baseline_can_be_explicitly_removed(self):
        selected={r["route_id"] for r in self.plan(baseline=False)["routes"] if r["selected"]}
        self.assertNotIn("saramin",selected)
    def test_unattempted_plan_fails_audit(self):
        errors,_=d.audit(self.plan(),self.catalog)
        self.assertTrue(any("unattempted" in x for x in errors))
    def test_completed_synthetic_records_pass_consistency(self):
        self.assertEqual(d.audit(self.completed(),self.catalog)[0],[])
    def test_naive_or_old_timestamp_fails(self):
        for value in ["2026-10-06T08:00:00","2026-10-05T08:00:00+09:00"]:
            run=self.completed()
            next(r for r in run["routes"] if r["selected"])["checked_at"]=value
            self.assertTrue(d.audit(run,self.catalog)[0])
    def test_access_failure_is_recorded_not_success(self):
        run=self.completed()
        row=next(r for r in run["routes"] if r["selected"])
        row.update(status="access_limited",evidence_level="attempt_only",
                   evidence_note="SYNTHETIC fetch failed",discovered_count=None)
        errors,warnings=d.audit(run,self.catalog)
        self.assertEqual(errors,[])
        self.assertTrue(warnings)
        row["status"]="checked"
        self.assertTrue(d.audit(run,self.catalog)[0])
    def test_false_exclusion_rejected(self):
        run=self.completed()
        next(r for r in run["routes"] if r["selected"]).update(status="excluded_by_user")
        self.assertTrue(d.audit(run,self.catalog)[0])
    def test_no_results_requires_zero_count(self):
        run=self.completed()
        next(r for r in run["routes"] if r["selected"]).update(status="no_relevant_results",discovered_count=3)
        self.assertTrue(d.audit(run,self.catalog)[0])
    def test_empty_coverage_cannot_pass(self):
        run=self.completed()
        for r in run["routes"]:
            r["selected"]=False
        self.assertTrue(d.audit(run,self.catalog)[0])
    def test_repost_cannot_be_official_recommendation(self):
        run=self.completed()
        run["jobs"]=[{"recommendation":"recommend","official_url":"https://example.invalid/repost",
                      "official_source_kind":"social","verified_at":"2026-10-06T08:00:00+09:00",
                      "current_status":"active","eligibility":"unknown"}]
        errors,_=d.audit(run,self.catalog)
        self.assertTrue(any("unofficial" in x for x in errors))
        self.assertTrue(any("verified eligibility" in x for x in errors))
    def test_channels_mode_has_no_job_recommendations(self):
        run=self.completed()
        run["request"]["mode"]="channels"
        run["jobs"]=[{"recommendation":"hold"}]
        self.assertTrue(d.audit(run,self.catalog)[0])

if __name__=="__main__":
    unittest.main()
