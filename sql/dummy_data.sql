-- =============================================
-- 1. student
-- =============================================
INSERT INTO student (student_id, name, birth_date, grade, class, number, gender, enrollment_year) VALUES
  ('b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '배수안', '2007-03-15', 2, 1, 5, '여', 2023),
  ('d1b8177d-91a3-4a29-b66e-95e64cd9e0c7', '이원정', '2006-11-08', 3, 2, 7, '남', 2022),
  ('62f0e1bb-0d6a-4d5e-9f14-b084a214c585', '우다연', '2007-06-01', 2, 3, 12, '여', 2023),
  ('3ce91873-93d2-4524-9c06-065be1d72f49', '이상원', '2006-04-22', 3, 1, 9, '남', 2022);

-- =============================================
-- 2. club
-- =============================================
INSERT INTO club (club_id, club_name, teacher, description) VALUES
  ('8c6e2cde-5765-4f20-8e52-3cfcdde31b0a', '쓰리디랩', '김지환',
   '메이커·발명동아리. 2023년에 설립됨. 3D 프린터랑 레이저커터로 아이디어를 바로 프로토타입으로 만듦. 매주 금요일 자유 제작 시간을 열어 서로 설계 리뷰를 했음. 지역 문제 해결용 작품을 팀별로 완성함.'),
  ('b2f9b3b5-3df4-431d-943f-8b1a4a7fd3f6', '타임슬립', '최명희',
   '역사탐방·연구동아리. 2022년에 시작됨. 매달 근현대사 유적지를 답사하며 사료 분석 세미나를 진행함. 현장 사진과 기록을 전시회로 묶어 공유했음. 활동 후 토론으로 관점을 확장했음.'),
  ('f1c9d6fe-bd63-4e17-9e30-84262f59b19e', '에코렌즈', '박건호',
   '생태사진·관찰동아리. 2023년 봄에 결성됨. 야산과 하천 생태를 계절별로 촬영해 기록함. DSLR 기초와 라이트룸 편집을 함께 익혔음. 결과물을 교내 로비에 전시해 반응이 좋았음.'),
  ('e7d4664d-e1dc-4c18-9a8f-fb1d682dcfeb', '로보스피어', '이하은',
   '로봇코딩·제작동아리. 2021년에 창립됨. 아두이노 기반 라인트레이서 로봇을 직접 제작함. 격주로 주행 알고리즘 튜닝 회의를 열었음. 하드웨어 고장도 스스로 해결하며 문제해결력을 길렀음.');

-- =============================================
-- 3. activity
-- =============================================
INSERT INTO activity (activity_id, student_id, activity_type, activity_name, description, activity_date, end_date, club_id, is_club) VALUES
  -- 배수안
  -- 동아리
  ('9e291648-1e17-4e2f-824e-bda4507cb9ef', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '동아리',
   '쓰리디랩 동아리에서 교내 메이커 페어 준비', '전시용 자동 급식 로봇을 설계함. 팀 리더로 부품 조달부터 조립까지 전 과정을 조율했음. 발표 때 작동 성공으로 관람객 관심을 끌었음.',
   '2024-04-10', '2024-05-20', '8c6e2cde-5765-4f20-8e52-3cfcdde31b0a', TRUE), -- 쓰리디랩
  ('31c023e5-24ec-4e22-8dc6-6f48c7fd1e65', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '동아리',
   '쓰리디랩 동아리에서 학교 기둥 미니어처 제작', '캠퍼스 건물 모형을 3D 프린터로 출력함. 색상 도색과 LED 조명 배선을 직접 배웠음. 완성품을 도서관 로비에 전시했음.', 
   '2024-06-05', '2024-06-18', '8c6e2cde-5765-4f20-8e52-3cfcdde31b0a', TRUE), -- 쓰리디랩
  ('934add6e-97c1-4d31-9176-13a694c3472e', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '동아리',
   '쓰리디랩 동아리에서 레이저커팅 워크숍 보조', '신입 동아리원을 대상으로 장비 안전 교육을 진행함. 간단한 우드 코스터 제작 시연을 했음. 참가자 만족도가 높았음.',
   '2024-09-02', '2024-09-02', '8c6e2cde-5765-4f20-8e52-3cfcdde31b0a', TRUE), -- 쓰리디랩
   -- 자율
  ('a2f7f3e1-4b5a-471c-808d-0f8b372ab16d', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '자율',
   '학교 홈페이지 개선 프로젝트', 'HTML, CSS, JavaScript를 사용하여 학교 홈페이지 디자인을 개편하고, 모바일 최적화 및 사용자 친화적 인터페이스를 설계함. 결과적으로 학교 웹사이트 방문자 수가 20% 증가함.',
   '2024-04-10', '2024-05-10', NULL, FALSE),
  ('29c023e5-24ec-4e22-8dc6-6f48c7fd1e65', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '자율',
   '교내 환경 보호 캠페인', '교내 쓰레기 분리배출 캠페인을 기획하고, 포스터와 소셜 미디어를 통해 홍보함. 이를 통해 교내 분리배출률이 30% 증가함.',
   '2024-06-01', '2024-06-30', NULL, FALSE),
  ('6f4add6e-97c1-4d31-9176-13a694c3472e', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '자율',
   '학생회 SNS 콘텐츠 제작', '학교 행사 및 공지사항을 SNS에 홍보하기 위한 콘텐츠를 기획하고 제작함. 결과적으로 학교 SNS 팔로워 수가 25% 증가함.',
   '2024-08-01', '2024-08-15', NULL, FALSE),
  -- 진로
  ('7e291648-1e17-4e2f-824e-bda4507cb9ef', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '진로',
   '진로 탐색 워크숍 참여', 'IT 및 데이터 분석 분야의 진로 워크숍에 참여하여 직업군에 대한 이해도를 높임. 이를 바탕으로 향후 진로 목표를 설정함.',
   '2024-03-15', '2024-03-16', NULL, FALSE),
  ('8d23c2e5-24ec-4e22-8dc6-6f48c7fd1e65', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '진로',
   '기업 연구소 방문 및 직무 체험', '대기업의 연구소를 방문하여 실무자들과의 Q&A 세션을 통해 직무에 대한 구체적인 이해를 얻음.',
   '2024-05-01', '2024-05-10', NULL, FALSE),
  ('9f5c8a8c-4ac9-4f8b-b44f-674dbf63b4f7', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '진로',
   '전문가 1:1 진로 상담', '진로 전문가와의 상담을 통해 다양한 직업군에 대한 심층 정보를 얻고, 진로 방향을 확립함.',
   '2024-08-10', '2024-08-12', NULL, FALSE),
  -- 특기적성
  ('9f3b2e56-5cf9-47ed-9350-2db5a6c542e5', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '특기적성',
   'AI 학습 모델 개발', 'Python과 TensorFlow를 사용하여 이미지 인식 시스템을 위한 머신러닝 모델을 개발하고, 모델의 정확도를 85% 이상으로 향상시킴.',
   '2024-04-02', '2024-04-30', NULL, FALSE),
  ('e57e3f4a-78cb-4d39-b1a2-eebd93cbd163', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '특기적성',
   '화학 실험 대회 참가', '화학 실험 대회에서 창의적인 실험 설계를 통해 실험 과제를 해결하고, 분석 능력과 창의성을 입증.',
   '2024-07-05', '2024-07-20', NULL, FALSE),
  ('fd23a5e6-4d0e-4897-b1c1-69d1f9c387a4', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '특기적성',
   '기술 창업 아이템 개발', '3D 모델링과 프로토타입 제작을 통해 새로운 기술 창업 아이템을 개발하고, 이를 발표하는 대회에 참가하여 긍정적인 반응을 얻음.',
   '2024-09-01', '2024-09-22', NULL, FALSE),

  -- 동아리 활동2 (에코렌즈)
  ('bfa0cd0e-6df6-44f1-9b99-d7ad86a9e888', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '동아리',
   '에코렌즈 동아리에서 하천 수질 조사 사진 촬영', 
   '하천의 수질을 조사하는 프로젝트에 참여하여, 수질 측정 후 오염이 심한 구간을 촬영하고, 해당 데이터를 그래프 형태로 시각화함. 이 데이터를 바탕으로 교내 환경 포스터를 제작하여 전시하였고, 환경 보호의 중요성에 대해 학생들에게 알림.',
   '2024-07-05', '2024-07-20', 'f1c9d6fe-bd63-4e17-9e30-84262f59b19e', TRUE),
  ('385e4ea9-95dc-4f50-bf7d-832799a660d6', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '동아리',
   '에코렌즈 동아리에서 생태 사진 공모전 출품',
   '강원도 산림지대에서 일출 풍경을 촬영하여 생태 사진 공모전에 제출. 후보정 과정에서 색감 조정과 구도 분석을 통해 사진의 미적 가치를 높였으며, 금상을 수상해 자신감을 얻었음.',
   '2024-09-01', '2024-09-22', 'f1c9d6fe-bd63-4e17-9e30-84262f59b19e', TRUE),
  -- 자율활동 (환경 또는 사진 관련)
  ('b5a2a9a1-8d2b-469f-bf7b-c6d1f66d1f7b', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '자율',
   '학교 내 환경 보호 캠페인 사진 전시회 기획', 
   '교내에서 진행된 **환경 보호 캠페인**을 주제로 **사진 전시회**를 기획하고, **환경 오염** 및 **자연 보호**를 주제로 한 사진들을 전시하여 학생들에게 환경 문제에 대한 경각심을 일깨움. 이 전시회는 학생들로부터 큰 호응을 얻었으며, 환경 보호에 대한 긍정적인 반응을 유도함.',
   '2024-04-15', '2024-04-30', NULL, FALSE),
  ('7c5a6c7b-09d4-42cf-8c8f-4b70f5c4ad75', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '자율',
   '디지털 포스터 제작 및 환경 문제 홍보', 
   '**디지털 포스터**를 제작하여 **환경 보호의 중요성**을 알리는 활동을 진행. 학교 행사나 외부 캠페인에 필요한 포스터를 디자인하여 학교 내 환경 문제 해결을 위한 메시지를 전달. 그 결과, 포스터는 여러 학생들로부터 긍정적인 반응을 얻었고, 환경 보호 활동 참여율이 증가함.',
   '2024-06-05', '2024-06-20', NULL, FALSE),
  -- 진로활동 (환경 또는 사진 관련)
  ('f2c8b2d4-a9c4-4e19-a81d-faa6cb8b2fc4', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '진로',
   '환경 사진작가 멘토링',
   '환경을 주제로 활동하는 사진작가와 1:1 멘토링을 받으며, 전문적인 촬영 기법과 사진 편집 기술을 배웠음. **자연 보호**와 **환경 문제**를 사진을 통해 어떻게 사회에 메시지로 전달할 수 있는지에 대해 알게 되었으며, 이를 통해 향후 환경 사진작가로서의 진로를 구체적으로 설정함.',
   '2024-07-01', '2024-07-05', NULL, FALSE),
  ('dfcb78a4-9bc6-4a24-87c9-f198d2557f34', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '진로',
   '자연 생태 보존 전문가 인터뷰',
   '자연 생태 보존과 관련된 전문가를 인터뷰하여, 환경 보호와 관련된 다양한 직무를 탐색. 생태 보존의 중요성과 **사진을 통한 환경 기록**의 역할에 대해 알게 되었으며, 향후 이 분야에서 전문가로 성장하기 위한 진로 방향을 구체화함.',
   '2024-06-10', '2024-06-12', NULL, FALSE),
  -- 특기적성 활동 (환경 또는 사진 관련)
  ('c1f6b8c2-5a2d-4389-bab9-68c238e58d3f', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '특기적성',
   '환경 사진 공모전 출품',
   '**환경 사진 공모전**에 참여하여, 자연 보호와 관련된 촬영 작품을 제출. **환경 보호**의 메시지를 담은 **사진**이 심사에서 높은 평가를 받았으며, **공모전에서 입상**하여 사진작가로서의 재능을 인정받음.',
   '2024-05-01', '2024-05-10', NULL, FALSE),
  ('031c75e2-3ea1-4939-bbd9-bd7b3c4b9e67', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '특기적성',
   '자연 환경 다큐멘터리 제작',
   '자연 환경과 생태계의 중요성을 담은 **다큐멘터리**를 제작하여 학교 행사에서 상영. 촬영부터 편집까지 직접 진행하면서 **환경 보호**와 관련된 메시지를 효과적으로 전달. 이를 통해 환경 문제에 대한 인식을 고취시키는 데 기여.',
   '2024-06-15', '2024-06-30', NULL, FALSE),

   

  -- 이원정
  ('db4a5f8d-1dcd-4714-9fa7-613ff9a274eb', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7', '동아리',
   '타임슬립 동아리에서 경복궁 야간 기행 기획', '탐방 동선과 해설 스크립트를 직접 작성함. 조명 변화에 맞춘 사진 포인트를 선정했음. 참가자 피드백이 긍정적이었음.',
   '2024-03-15', '2024-03-16', 'b2f9b3b5-3df4-431d-943f-8b1a4a7fd3f6', TRUE), --타임슬립
  ('915e4ea9-95dc-4f50-bf7d-832799a660d6', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7', '동아리',
   '타임슬립 동아리에서 근대 인물 카드뉴스 제작 프로젝트 참여', '7명의 독립운동가 생애를 카드뉴스로 제작함. 자료 조사와 일러스트 작업을 분담했음. SNS 게시 후 조회 수가 높았음.',
   '2024-05-01', '2024-05-25', 'b2f9b3b5-3df4-431d-943f-8b1a4a7fd3f6', TRUE), --타임슬립
  ('4e76c80a-acdb-4e8b-ae05-6e57df06afde', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7', '동아리',
   '타임슬립 동아리에서 문화재 해설사 멘토링', '전문 해설사와 1:1 멘토링을 받았음. 실전 투어에서 관객 질문에 직접 답변함. 진로 방향을 구체화했음.',
   '2024-08-10', '2024-08-12', 'b2f9b3b5-3df4-431d-943f-8b1a4a7fd3f6', TRUE), --타임슬립
   -- 자율활동
  ('d7f7b784-15b6-4072-96a5-a8d9f49eac26', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7', '자율',
   '학교 행사 프로그램 기획', '학교 축제에서 학생들이 참여할 수 있는 다양한 프로그램을 기획하고 운영함. 참여율이 40% 증가하며, 학생들의 창의력을 발휘할 기회를 제공.',
   '2024-04-10', '2024-04-20', NULL, FALSE),
  ('937a6c7b-09d4-42cf-8c8f-4b70f5c4ad75', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7', '자율',
   '디지털 포스터 제작 및 전시', '학교 행사 홍보를 위한 디지털 포스터를 디자인하고, 학교 전시회에서 이를 전시하여 디자인 역량을 발휘함.',
   '2024-06-05', '2024-06-20', NULL, FALSE),
  ('f2a54402-22b7-457f-a0a2-2ef083bc47a0', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7', '자율',
   '자율적 운동 프로그램 운영', '학생들의 체력 증진을 위해 자율 운동 프로그램을 기획하고 운영함. 참여 학생들의 체력 지수가 15% 향상됨.',
   '2024-08-01', '2024-08-31', NULL, FALSE),
  -- 진로활동
  ('e2c2d4b3-72fc-4b43-a54f-bec6c813f06c', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7', '진로',
   '역사 관련 전문가 인터뷰', '역사 분야의 전문가와 1:1 인터뷰를 통해 역사학에 대한 구체적인 진로 조언을 받음. 역사학자로서의 경로와 준비 과정을 이해.',
   '2024-05-10', '2024-05-12', NULL, FALSE),
  ('dfcb78a4-9bc6-4a24-87c9-f198d2557f65', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7', '진로',
   '역사 유적지 탐방', '경주 불국사와 안동 하회마을 등 주요 역사 유적지를 탐방하며, 문화재 보호 전문가와의 현장 토론을 통해 역사적 가치와 보존의 중요성에 대해 배움. 해당 분야의 진로에 대한 구체적인 계획을 세움.',
   '2024-06-15', '2024-06-20', NULL, FALSE),
  ('35eaf7c5-7a58-4205-b990-5a57b5c3b6a7', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7', '진로',
   '문화유산 보호 활동 참여', '문화유산 보호 단체에서 자원봉사를 하며, 문화재 보존 작업과 관련된 실제 업무를 경험.',
   '2024-07-01', '2024-07-20', NULL, FALSE),
  -- 특기적성 활동
  ('c1f6b8c2-5a2d-4389-bab9-68c238e585ff', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7', '특기적성',
   '역사 관련 에세이 공모전 출품', '문화재 보호와 역사적 가치에 관한 에세이를 작성하여 공모전에 출품, 우수작으로 선정됨.',
   '2024-04-01', '2024-04-10', NULL, FALSE),
  ('2a1c75e2-3ea1-4939-bbd9-bd7b3c4b9e67', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7', '특기적성',
   '역사 다큐멘터리 제작', '우리나라 근대 역사에 대한 다큐멘터리를 제작하여, 학교 행사에서 상영하며 사회적 관심을 불러일으킴.',
   '2024-05-15', '2024-05-30', NULL, FALSE),
  ('1f2ac9b1-1fe7-49e4-8de1-948d924e9b52', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7', '특기적성',
   '사회적 이슈에 대한 연구 발표', '현재 사회적 이슈인 고용 불안정 문제에 대해 연구하고, 결과를 발표하여 학급 내에서 큰 반향을 일으킴.',
   '2024-06-05', '2024-06-20', NULL, FALSE),


  -- 우다연
INSERT INTO activity (activity_id, student_id, activity_type, activity_name, description, activity_date, end_date, club_id, is_club) VALUES

  ('c2f7a784-05b6-4072-96a5-a8d9f49eac25', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585', '동아리',
   '에코렌즈 동아리에서 봄철 나비 관찰 전시', '교내 화단에서 촬영한 나비 12종을 분류함. RAW 현상과 매크로 렌즈 활용법을 공유했음. 결과 사진을 액자로 만들어 전시했음.',
   '2024-04-02', '2024-04-30', 'f1c9d6fe-bd63-4e17-9e30-84262f59b19e', TRUE), -- 에코렌즈
  ('caad5a46-8216-4cab-9614-809969c3e15b', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585', '동아리',
   '에코렌즈 동아리에서 하천 수질 조사 사진 촬영', '정수 TDS 측정 후 오염 구간을 촬영함. 촬영 데이터를 그래프로 시각화했음. 결과를 환경 포스터로 제작해 게시했음.',
   '2024-07-05', '2024-07-20', 'f1c9d6fe-bd63-4e17-9e30-84262f59b19e', TRUE), -- 에코렌즈
  ('1a5ce3f0-d41e-4a51-a526-87b0d800b1c8', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585', '동아리',
   '에코렌즈 동아리에서 생태 사진 공모전 출품', '강원도 산림지대 일출 풍경을 촬영해 공모전에 제출했음. 후보정 과정에서 색감 밸런스를 조정했음. 금상을 수상해 자신감을 얻었음.',
   '2024-09-01', '2024-09-22', 'f1c9d6fe-bd63-4e17-9e30-84262f59b19e', TRUE), -- 에코렌즈
    -- 자율활동
  ('d2f7a784-05b6-4072-96a5-a8d9f49eac26', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585', '자율',
   '지역 환경 보호 캠페인', '지역 내 환경 보호를 위한 캠페인에 참여하여, 재활용을 장려하고 지역 청소 활동을 진행함. 지역 주민들과 협력하여 환경 보호 의식을 고취.',
   '2024-04-05', '2024-04-20', NULL, FALSE),
  ('caad5a46-8216-4cab-9614-809969c3e15c', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585', '자율',
   '학교 내 재활용 프로그램 개선', '교내 재활용 프로그램의 개선을 위해 교내 쓰레기 분리배출 시스템을 분석하고 개선안을 제시함. 재활용률을 20% 향상시킴.',
   '2024-06-01', '2024-06-15', NULL, FALSE),
  ('1a5ce3f0-d41e-4a51-a526-87b0d800b1c9', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585', '자율',
   '환경 보호 관련 강연 참여', '환경 문제 해결을 위한 강연에 참여하여, 환경 보호에 대한 다양한 관점을 배우고, 이를 바탕으로 학교 내 환경 보호 교육 프로그램을 제안.',
   '2024-07-10', '2024-07-15', NULL, FALSE),
  -- 진로활동
  ('f2c8b2d4-a9c4-4e19-a81d-faa6cb8b2fc6', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585', '진로',
   '환경 공학 관련 진로 탐색', '환경 공학 분야의 전문가와 1:1 상담을 통해 환경 문제 해결을 위한 기술적 접근법에 대해 배움. 해당 분야의 직무와 진로 가능성에 대해 구체적으로 알아봄.',
   '2024-07-01', '2024-07-05', NULL, FALSE),
  ('3f2b7d5f-ea2d-4c0a-b29d-777f21d9e0fd', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585', '진로',
   '환경 보호 관련 NGO 체험', '환경 보호 NGO에서 진행하는 활동에 참여하여, 환경 문제 해결을 위한 조직적인 활동과 리더십을 경험.',
   '2024-07-15', '2024-07-20', NULL, FALSE),
  ('dfe345e1-cf63-433d-a756-bd64b70e7d88', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585', '진로',
   '지속 가능한 에너지 개발 세미나 참여', '지속 가능한 에너지 개발에 관한 세미나에 참여하여, 재생 가능 에너지와 관련된 직업과 경로를 탐색.',
   '2024-08-01', '2024-08-05', NULL, FALSE),
  -- 특기적성 활동
  ('fa24556e-3301-47b0-83f9-53948d674c58', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585', '특기적성',
   '환경 사진 전시회 기획', '환경 보호를 주제로 한 사진전시회를 기획하고, 다양한 환경 관련 사진을 전시하여 환경 보호 메시지를 전달.',
   '2024-05-01', '2024-05-10', NULL, FALSE),
  ('b284df58-70be-4756-81c7-85b8e2687a70', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585', '특기적성',
   '환경 사진 공모전 출품', '자연 환경과 오염 문제에 대한 사진을 공모전에 제출하여, 사회적 메시지를 전달하고 공모전에서 우수상을 받음.',
   '2024-06-10', '2024-06-20', NULL, FALSE),
  ('a64b7866-e567-4c6f-88b2-e703ea44ccfc', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585', '특기적성',
   '디지털 사진 기술 교육', '디지털 사진 촬영과 편집 기술을 배워, 환경과 자연을 주제로 한 사진 프로젝트를 진행.',
   '2024-07-01', '2024-07-10', NULL, FALSE),


  -- 이상원
  ('735b5eab-9087-4921-9f96-35971ff90cd0', '3ce91873-93d2-4524-9c06-065be1d72f49', '동아리',
   '로보스피어 동아리에서 교내 로봇 경진대회 준비', '팀 주행 알고리즘을 설계함. 회로 납땜과 프레임 설계까지 주도했음. 예선 랩타임 1위를 기록했음.',
   '2024-02-20', '2024-04-10', 'e7d4664d-e1dc-4c18-9a8f-fb1d682dcfeb', TRUE), -- 로보스피어 
  ('810b9c1c-80c4-47bd-aeb1-64c7d2d6ec42', '3ce91873-93d2-4524-9c06-065be1d72f49', '동아리',
   '로보스피어 동아리에서 라인트레이서 코드 최적화', 'PID 값 자동 조정 스크립트를 작성함. 센서 노이즈를 평균화해 주행 흔들림을 줄였음. 주행 시간 15% 단축에 성공했음.',
   '2024-05-12', '2024-05-25', 'e7d4664d-e1dc-4c18-9a8f-fb1d682dcfeb', TRUE), -- 로보스피어 
  ('a2d76032-0da2-4f23-9e29-88ea46564735', '3ce91873-93d2-4524-9c06-065be1d72f49', '동아리',
   '로보스피어 동아리에서 대학 로봇공학 캠프 참가', 'ROS 기초 강의를 수강함. 팀 프로젝트로 자율 주행 카트를 제작했음. 대학 연구실 분위기를 직접 체험했음.',
   '2024-08-01', '2024-08-05', 'e7d4664d-e1dc-4c18-9a8f-fb1d682dcfeb', TRUE), -- 로보스피어 
   -- 자율활동
  ('b2f9d1e4-66fc-43b1-84fa-6996b8a3f6ff', '3ce91873-93d2-4524-9c06-065be1d72f49', '자율',
   '로봇 공학 관련 온라인 강의 수강', '로봇 공학과 관련된 온라인 강의를 수강하고, 다양한 알고리즘 및 로봇 제어 시스템에 대해 학습.',
   '2024-04-10', '2024-05-10', NULL, FALSE),
  ('f5d76032-1da2-4f23-9e29-88ea46564736', '3ce91873-93d2-4524-9c06-065be1d72f49', '자율',
   '자율 주행 기술 탐구', '자율 주행 자동차의 기술적 발전과 미래를 탐구하는 프로젝트를 진행하고, 관련 논문을 작성.',
   '2024-05-15', '2024-06-01', NULL, FALSE),
  ('830b9c1c-80c4-47bd-aeb1-64c7d2d6ec42', '3ce91873-93d2-4524-9c06-065be1d72f49', '자율',
   '로봇 공학 관련 책 독서', '로봇 공학의 이론과 실습을 다룬 책을 읽고, 이를 바탕으로 새로운 아이디어를 제시하는 독서 활동.',
   '2024-06-10', '2024-06-20', NULL, FALSE),
  -- 진로활동
  ('b1c2d4b3-72fc-4b43-a54f-bec6c813f06c', '3ce91873-93d2-4524-9c06-065be1d72f49', '진로',
   '로봇 공학 관련 기업 인턴십', '로봇 공학 관련 기업에서 2주간의 인턴십을 통해, 실제 로봇 개발 과정과 프로그래밍을 체험.',
   '2024-06-01', '2024-06-15', NULL, FALSE),
  ('dfnf78a4-9bc6-4a24-87c9-f198d2557f65', '3ce91873-93d2-4524-9c06-065be1d72f49', '진로',
   '자율 주행 기술 박람회 참가', '자율 주행 기술에 관한 박람회에 참가하여 최신 기술과 산업 동향에 대해 배우고, 관련 직업군을 탐색.',
   '2024-07-05', '2024-07-10', NULL, FALSE),
  ('39eaf7c5-7a58-4205-b990-5a57b5c3b6a7', '3ce91873-93d2-4524-9c06-065be1d72f49', '진로',
   '로봇 기술 전문가와의 1:1 멘토링', '로봇 기술 전문가와의 멘토링을 통해 진로를 구체화하고, 필요한 기술 및 경험을 논의.',
   '2024-08-01', '2024-08-10', NULL, FALSE),
  -- 특기적성 활동
  ('n4d6b8c2-5a2d-4389-bab9-68c238e585ff', '3ce91873-93d2-4524-9c06-065be1d72f49', '특기적성',
   '로봇 공학 관련 문제 해결 대회 참가', '로봇 공학 관련 문제 해결 대회에 참가하여 창의적인 문제 해결 능력을 발휘.',
   '2024-04-01', '2024-04-10', NULL, FALSE),
  ('2a5c93e2-3ea1-4939-bbd9-bd7b3c4b9e67', '3ce91873-93d2-4524-9c06-065be1d72f49', '특기적성',
   '로봇 모델링 및 설계', '로봇 모델링과 설계를 통해 창의적인 기계 구조를 제작하고, 이를 실험하여 성능을 최적화.',
   '2024-05-15', '2024-05-25', NULL, FALSE),
  ('3f7ac9b1-1fe7-49e4-8de1-948d924e9b52', '3ce91873-93d2-4524-9c06-065be1d72f49', '특기적성',
   '로봇 제어 알고리즘 작성', '자율 주행 로봇의 제어 알고리즘을 작성하여, 센서 데이터를 기반으로 정확한 경로 추적을 구현.',
   '2024-06-01', '2024-06-15', NULL, FALSE);

-- =============================================
-- 4. award
-- =============================================
INSERT INTO award (award_id, student_id, award_name, awarding_body, award_level, award_date, description) VALUES
  ('0c36b4bc-3d89-418a-9104-bd60fe973965', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda',
   '교내 메이커 페어 최우수상', '학교 공학부', '교내', '2024-06-15',
   '자동 급식 로봇이 창의성과 실용성을 동시에 인정받음. 참가팀 18팀 가운데 최고 점수를 획득했음. 제작 과정 기록이 호평을 받았음.'),
  ('b62a1f9e-0e27-45e1-bb21-5ecf07e621e4', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7',
   '전국 역사 UCC 공모전 은상', '한국역사학회', '교외', '2024-11-03',
   '조선 후기 생활사를 주제로 10분짜리 영상 제작함. 전국 200팀 중 2위임. 현장 인터뷰와 드론 촬영 기법이 신선하다는 평가를 받았음.'),
  ('6acf4338-cc26-4f7e-9aee-59b3e7fc02ad', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585',
   '청소년 생태 사진전 금상', '환경부', '교외', '2024-09-22',
   '새벽 습지에서 촬영한 왜가리 비행 사진이 입상함. 심사위원단이 색상 대비와 구도에 높은 점수를 줬음. 참가 인원 350명 규모였음.'),
  ('e2b9fa48-5002-4d4c-b1a0-312091071b7c', '3ce91873-93d2-4524-9c06-065be1d72f49',
   '전국 고교 로봇대회 우승', '대한로봇협회', '교외', '2024-10-10',
   '자율 주행 부문에서 최고 기록 달성함. 전국 45개교가 참가했음. 주행 안정성과 코드 효율성이 심사 기준을 압도했음.');

-- =============================================
-- 5. grade
-- =============================================
INSERT INTO grade (grade_id, student_id, semester, year, subject, score, description) VALUES
  -- 배수안
  ('5c8dbe5a-0b3e-4993-8d5b-a6c5dd6a2e10', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '1학기', 2024, '과학', 'A',
   '화학 반응식 균형 맞추기는 능숙했음. 전기화학 전위 계산에서 전극 기호 순서를 가끔 헷갈렸음. 그래도 실험 보고서 형식은 깔끔했음.'),
  ('cb902e0a-2da0-440e-9aa4-94e00387d4a1', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '2학기', 2024, '수학', 'B',
   '미적분의 도함수 계산은 빠르고 정확했음. 반면 부정적분을 활용한 면적 계산에서 치환법 적용이 흔들렸음. 풀이 과정 기록은 성실했음.'),
  ('61fcd98b-f0bf-4be8-96f9-b8379ee54c8f', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '1학기', 2024, '영어', 'C',
   '듣기 파트에서 세부 정보까지 잡아냈음. 에세이에서 가정법 구조 사용이 어색했음. 연결어 다양성이 부족했음.'),
  ('9e316d23-0bc2-4c59-99f9-b859a1e18eee', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda', '2학기', 2024, '사회', 'D',
   '정치 단원 핵심 개념을 자주 놓쳤음. 입법 절차 순서를 거꾸로 기억했음. 뉴스 기사 예시는 적절히 찾아왔음.'),

  -- 이원정
  ('af3af7a9-2c28-4ada-8667-8da4fbad3c72', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7', '1학기', 2024, '사회', 'A',
   '현대사 사건을 연표로 재구성하는 능력이 뛰어났음. 시사 논평과 연결해 통찰을 보여줬음. PPT 시각 효과가 단조로웠음.'),
  ('9d3e1967-52bf-4c9c-9e80-830627baad42', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7', '2학기', 2024, '영어', 'B',
   '리딩 지문 핵심을 빠르게 요약했음. 스피킹에서 강세와 억양이 일정치 않아 전달력이 약했음. 어휘 선택은 다양했음.'),
  ('f1c8b6ac-1071-4d7a-8b7c-b44827093a21', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7', '1학기', 2024, '과학', 'C',
   '세포 호흡 경로는 이해했음. 광합성 생성물 비율을 자주 틀렸음. 실험 질문에 근거 제시가 부족했음.'),
  ('ecb7a7e7-5fb7-4a0d-8cd0-4c75639c44e6', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7', '2학기', 2024, '수학', 'D',
   '닮음 조건을 정확히 구분하지 못했음. 증명 과정에서 이유 쓰기를 자주 생략했음. 기초 계산 정확도는 유지했음.'),

  -- 우다연
  ('eadb8a3b-d01d-4a15-83ec-26f3c1466699', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585', '1학기', 2024, '영어', 'A',
   '프레젠테이션 도표 설명이 유창했음. 즉석 질의응답도 자신감 있게 처리했음. 철자 오류가 가끔 있었음.'),
  ('b63917b0-0eed-4fca-82c1-89e3f964a26b', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585', '2학기', 2024, '과학', 'B',
   '굴절률 측정 실험 값이 안정적이었음. 파동 간섭 무늬 공식 적용을 헷갈렸음. 보고서 형식은 규정에 맞게 작성했음.'),
  ('c36bfd52-07bd-4595-9cf7-9f7a1ed06e75', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585', '1학기', 2024, '사회', 'C',
   '윤리와 사상에서 칸트 의무론은 정확히 설명했음. 그러나 데카르트 방법적 회의를 요점을 놓쳤음. 반론 근거가 약했음.'),
  ('e22b310f-f2cb-4ec3-b9b7-3777d9898cab', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585', '2학기', 2024, '수학', 'D',
   '확률 분포 구간 설정을 제대로 잡지 못했음. 공식 암기만 의존해 응용 문제가 막혔음. 과제 제출 지연이 잦았음.'),

  -- 이상원
  ('5d1a42a5-92eb-47e4-8c3c-e88019ae2814', '3ce91873-93d2-4524-9c06-065be1d72f49', '1학기', 2024, '수학', 'A',
   '벡터 내적과 외적 계산을 오류 없이 수행했음. 다변수 편미분도 정확했음. 그래프 주석 표기가 간략했음.'),
  ('f4d149c4-8c9d-4c74-9c8a-5f5ef6bb3c2d', '3ce91873-93d2-4524-9c06-065be1d72f49', '2학기', 2024, '과학', 'B',
   '센서 실험에서 오차 원인을 잘 분석했음. 전자기 유도 단위 변환 실수가 있었음. 보고서 결론 정리는 충실했음.'),
  ('0a54a0d5-2f1f-4e71-8edd-935317e8b2e5', '3ce91873-93d2-4524-9c06-065be1d72f49', '1학기', 2024, '영어', 'C',
   '주제문 찾기는 빠르고 정확했음. 서평에서 비유 표현이 반복돼 표현력이 단조로웠음. 단어장 복습은 꾸준했음.'),
  ('3576cb47-54aa-4c3b-a30f-7e1cdd209cb7', '3ce91873-93d2-4524-9c06-065be1d72f49', '2학기', 2024, '사회', 'D',
   'GDP 성장률 계산과 같은 지표 해석이 취약했음. 팀 프로젝트 준비가 부족해 역할 수행에 공백이 있었음. 기사 스크랩은 꾸준히 했음.');


-- =============================================
-- 6. subject_detail
-- =============================================
INSERT INTO subject_detail (detail_id, student_id, grade_id, subject, semester, year, category, description) VALUES
  -- 배수안
  ('a3ff4860-c347-41f7-b44f-766dfe4d0eab', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda',
   '5c8dbe5a-0b3e-4993-8d5b-a6c5dd6a2e10',  -- 과학 A
   '과학', '1학기', 2024, '활동',
   '중력 가속도 측정 실험에서 타이머 정확도를 개선했음. 데이터 분산을 그래프로 분석했음. 동료와 결과 비교 후 원인을 토론했음.'),
  ('0e4bb8e5-5564-4e12-b6fa-2fb089751e26', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda',
   'cb902e0a-2da0-440e-9aa4-94e00387d4a1',  -- 수학 B
   '수학', '2학기', 2024, '발표',
   '삼각함수 그래프 주기를 시각 자료로 설명했음. 청중 질문에 예시를 통해 답변했음. 발표 흐름이 매끄러웠음.'),

  -- 이원정
  ('5e3e2ae3-4523-4e2b-8c09-cc3e679a54c6', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7',
   'af3af7a9-2c28-4ada-8667-8da4fbad3c72',  -- 사회 A
   '사회', '1학기', 2024, '수행평가',
   '기후 난민 이슈를 자료집으로 정리했음. 인터뷰 질문지를 직접 설계했음. 결론에서 대안 정책을 제시했음.'),
  ('6a68552b-db37-41ee-b4f2-52f4b63f2a4c', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7',
   '9d3e1967-52bf-4c9c-9e80-830627baad42',  -- 영어 B
   '영어', '2학기', 2024, '독서',
   '소설 “The Giver”를 읽고 사회 체제 분석 에세이를 작성했음. 주인공 심리를 비판적으로 해석했음. 토론에서 의견을 명확히 제시했음.'),

  -- 우다연
  ('13905ecd-1d0c-4d62-9d21-6f6f467fd6ba', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585',
   'eadb8a3b-d01d-4a15-83ec-26f3c1466699',  -- 영어 A
   '영어', '1학기', 2024, '발표',
   'TED 식 발표 형식을 참고해 “Zero Waste” 주제를 소개했음. 청중 참여 퀴즈를 넣어 몰입도를 높였음. 시간 관리가 정확했음.'),
  ('5d317561-9d11-47fe-9434-880e4e96c6ea', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585',
   'b63917b0-0eed-4fca-82c1-89e3f964a26b',  -- 과학 B
   '과학', '2학기', 2024, '활동',
   '학교 텃밭 식물 성장 관찰 일지를 작성했음. 생장 조건 변화를 기록했음. 발표 때 그래프를 사용해 설명했음.'),

  -- 이상원
  ('66e326fa-1581-4ab5-9d51-34e6ceb7b5b0', '3ce91873-93d2-4524-9c06-065be1d72f49',
   '5d1a42a5-92eb-47e4-8c3c-e88019ae2814',  -- 수학 A
   '수학', '1학기', 2024, '발표',
   '자율 주행 알고리즘과 미분 방정식 관계를 설명했음. 예시 코드를 시연해 이해를 도왔음. 청중 질문에 추가 그래프로 답변했음.'),
  ('b34bcbd1-7e62-4b6c-b4e8-2af4b9626f59', '3ce91873-93d2-4524-9c06-065be1d72f49',
   'f4d149c4-8c9d-4c74-9c8a-5f5ef6bb3c2d',  -- 과학 B
   '과학', '2학기', 2024, '활동',
   '초음파 센서 측정 오차를 실험으로 검증했음. 오차 범위를 수식으로 정리했음. 개선안으로 필터링 코드를 제안했음.');


-- =============================================
-- 7. volunteer
-- =============================================
INSERT INTO volunteer (volunteer_id, student_id, organization, description, volunteer_date, hours) VALUES
  ('ca4a7caa-3fdb-4e58-8fad-aeee9842e11a', 'b6e6b463-6ba0-4d75-90fb-ae9489e60cda',
   '시립 정보도서관', '메이커스페이스에서 초등학생 3D 펜 체험 프로그램을 도왔음. 기기 안전 지도를 맡았음. 참여 아동이 완성품을 기뻐해 보람 있었음.',
   '2024-07-18', 4),
  ('6bcff2d8-bdf6-48b7-9f40-9c6adcc18d45', 'd1b8177d-91a3-4a29-b66e-95e64cd9e0c7',
   '문화재 해설 행사', '외국인 관광객 대상 해설 부스를 운영했음. 영어∙일어 번역을 번갈아 맡았음. 관객 호응이 높아 뿌듯했음.',
   '2024-05-02', 6),
  ('3a2ff025-fd5b-4ac2-9f2e-a0d744960770', '62f0e1bb-0d6a-4d5e-9f14-b084a214c585',
   '환경단체 나무심기', '하천 둔치에 버드나무 40주를 옮겨 심었음. 사진 기록으로 성장 과정을 추적하기로 했음. 팀워크가 잘 맞았음.',
   '2024-03-29', 5),
  ('8fae774d-0a4a-4ab1-bd18-a4709a953c8c', '3ce91873-93d2-4524-9c06-065be1d72f49',
   '청소년 과학관', '로봇 체험 부스에서 조립 시연을 진행했음. 어린이 질문을 쉽게 풀어 설명했음. 하루 동안 300명 이상이 체험했음.',
   '2024-08-05', 7);
