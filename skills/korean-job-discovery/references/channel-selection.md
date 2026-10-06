# Channel selection

| Track | Complementary sources | Duty aliases |
| --- | --- | --- |
| it | Jumpit, RocketPunch, Superookie, InThisWork, JobPlanet; OKKY if accessible | QA, 검증, TestBed, IT Support, 전산, Linux, 데이터 운영 |
| junior | Superookie, LINKareer, InThisWork, relevant university boards | 신입, 인턴, 주니어, 경력무관, 운영, 사무지원 |
| finance | KOFIA member hiring, Peoplenjob, LinkedIn | 리서치 RA, 운용지원, 펀드·채권평가, 금융데이터 |
| rnd | RND JOB, KIRD/K-club, NST and institute careers | 연구지원, 시험평가, 실증, 임베디드, 로봇, 머신비전 |
| public | JOB-ALIO, Cleaneye Job+, GoJobs | NCS 정보통신, 기술직, 공무직, 전산, 청년인턴 |
| foreign | Peoplenjob, KOTRA board, LinkedIn | Korea/Seoul + Support/Operations/Research/QA |
| overseas | WorldJob+, LinkedIn | country + occupation; visa/workplace |
| startup | THE VC, Startup Alliance, D.CAMP, TIPS, RocketPunch | industry/technology → employer → careers |
| bio | BRIC if accessible, KIRD/K-club, lab careers | 학사 연구원, 연구인턴, 실험지원 |

General boards: Saramin, Wanted, Catch, Jasoseol, JobKorea, Incruit, Work24.
These can overlap. Respect user-required/excluded sources. The helper selects
these seven by default; --no-baseline removes them for explicitly limited tasks.

Regional job portals, technoparks, universities and industrial parks must match
the requested region. Busan/Gyeongnam seeds are examples, not nationwide defaults.
Find equivalent official sources elsewhere. A publicly readable school post
does not prove eligibility for school recommendation.

LinkedIn/company/recruiter public X and Instagram posts can reveal leads.
GeekNews and Disquiet are incidental company/product signals; a current dedicated
hiring board is not asserted. Do not mandate a particular curator for all users.

## Modes and expansion
- channels: route operation, filters, audience and methods; no individual-job claims.
- broad: multiple employers/jobs; use an applicable company-directory path and
  ATS-domain or PDF supplement when available.
- company: official employer careers/ATS plus employer-name and duty searches;
  do not collect unrelated company rosters.

Start with a complementary set (usually two specialist sources per track);
--per-track changes that helper heuristic. This is not a universal fixed count.
Regional/university and mandatory local instructions can increase coverage.

Sparse results: adjust duty aliases and remaining related sources, not hard
eligibility or geography. Recheck dated seed observations. Record selection and
nonselection reasons separately; agent-chosen omissions are not excluded_by_user.

## Query templates (not executed searches)
```text
site:career.greetinghr.com (신입 OR 인턴) (QA OR 검증 OR "데이터 운영")
site:jobs.lever.co (Korea OR Seoul) (support OR operations OR QA)
site:boards.greenhouse.io (Korea OR Seoul) (testing OR research OR data)
site:jobs.ashbyhq.com (Korea OR Seoul) (operations OR support OR QA)
site:ac.kr (채용 OR 추천채용) (전산 OR 로봇 OR 연구지원) (신입 OR 인턴)
site:ac.kr filetype:pdf 채용 (시험 OR 검증 OR 기술지원)
("데이터 운영" OR "Data Operations" OR "데이터 검수") 채용
("업무 자동화" OR "AI 운영" OR "프로세스 개선") 채용
```
Portal search may not support OR/quotes: search aliases separately. Read the
underlying source rather than snippets. Employer custom domains and unindexed
pages still need inspection through its official homepage.
