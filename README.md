# About

성균관대 양자정보센터에서 주관한 DWave 교육(29.11.23-01.12.23)에서 코드 부분을 정리한 Repo.

참고사항
1. 모든 코딩 실습은 Github Codespace에서 진행되었음.
2. 대부분의 실행이 DWave의 Cloud QPU에서 진행되었음. 지금은 해당 QPU를 사용할 수 없음(학생은 Limited Access는
  있다고 함). 그래서 아마 안 돌아갈거임.
3. 나는 교육용으로 받은 Leap으로 했음.(https://cloud.dwavesys.com/)
4. 위 링크에 있는 Solver API Token을 이용하려면
   1. dwave-ocean-sdk가 설치된 venv에는 이제 dwave 명령어가 생김
   2. dwave config create 치고 나서 위의 token 입력하면 됨
   3. 성공하면 dwave ping 명령어가 먹힘
   4. 만약 token 없으면
   - dwave auth login치고 나오는 링크에서 auth해주고
   - dwave auth get 하면 auth 주는 것 같기도 하다 안해봐서 모름
5. 모든 코드는 링크 그대로 베낀거 + 답 쓴거 몇개


## 1. original_program.py

https://github.com/dwave-training/graph-mapping/blob/master/original_program.py

- 29.11.23(1일차)
- 1-1-38pp Antennas Program
- 코딩은 따로 없고 그냥 실행해보는 실습이었음
- QUBO에 대해 고민하기 전에, 그냥 그래프를 통째로 넣는 것도 된다고 알려주려는 실습
- 결과로 png 두개가 생김
- 그냥 networkx 패키지랑 호환이 좋다는 거의 강조인듯...?

## 2. hss_exercise.py

https://github.com/dwave-training/traveling-salesperson/blob/master/hss_exercise.py

- 29.11.23(1일차)
- 1-2-25pp Travelling Salesman
- 그냥 sampler같은거 instantiate 시키는 등 개념 익히기 용 예제인듯..?
## 3. npp.py

https://github.com/dwave-training/number-partitioning/blob/master/npp.py

- 29.11.23(1일차)
- 2-2-20pp ~ 2-2-36pp Number Partitioning
- 중요 예제, QUBO 만드는 개념과 Chain Strength에 대해 알 수 있다.

## 4. clustering.py

https://github.com/dwave-examples/clustering/blob/master/clustering.py

- 30.11.23(2일차)
- 2-1-31pp Clustering
- 코드보다는 Inspector를 해보려고 함
- Inspector는 지금은 그냥 슥 보기만 하면 될듯? QPU Usage나 Topology 최적화 용도같음.


## 5. friends_enemies_hybrid.py

https://github.com/dwave-training/social-networks/blob/main/friends_enemies_hybrid.py

- 30.11.23(2일차)
- 1-2-51pp Friends and Enemies
- QUBO 식을 구성할 때, 1-2-44~1-2-46pp에서 구한 Same/Diff 식을 사용한 게 중요
- BQM에 add_linear 및 add_quadratic 함수 적용도 중요한 듯


## 6. choosing_boxes.py

https://github.com/dwave-training/choosing-boxes/blob/master/choosing_boxes.py

- 30.11.23(2일차)
- 2-2-51pp Choosing Boxes


## 7. scheduling_preferences.py

https://github.com/dwave-training/employee-scheduling

- 01.12.23(3일차)
- 3-1-5pp Employee Scheduling
- 3일차는 여러 파일에 걸쳐서 Develop하는 형식으로 함(아래 순서)
  - scheduling_preferences.py
  - scheduling_addemployees.py
  - scheduling_restrictions.py


## 8. portfolio.py

https://github.com/dwave-training/portfolio-optimization

- 01.12.23(3일차)
- 3-1-8pp Portfolio Optimization
- 3일차는 여러 파일에 걸쳐서 Develop하는 형식으로 함(아래 순서)
  - exercise_1.py
  - exercise_2.py
  - exercise_3.py