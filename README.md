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

1. 코딩은 따로 없고 그냥 실행해보는 실습이었음
2. QUBO에 대해 고민하기 전에, 그냥 그래프를 통째로 넣는 것도 된다고 알려주려는 실습
3. 결과로 png 두개가 생김
4. 그냥 networkx 패키지랑 호환이 좋다는 거의 강조인듯...?

## 2. hss_exercise.py

https://github.com/dwave-training/traveling-salesperson/blob/master/hss_exercise.py
- 1-2-25pp Travelling Salesman
