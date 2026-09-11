---
title: "7강. 곱측도, Fubini, 독립성 — iid의 정확한 의미"
date: 2026-09-09
lastmod: 2026-09-11
draft: false
math: true
description: "데이터셋을 P^n에서 뽑는다는 한 줄이 측도론적으로 무엇을 주장하는가. 독립성은 공동분포가 곱측도라는 구조적 명제이고, 그 위의 적분을 반복적분으로 바꾸는 도구가 Tonelli와 Fubini다."
summary: "각 좌표의 분포만으로는 공동분포가 결정되지 않는다는 관찰에서 출발해, 두 측도공간을 곱 σ-대수와 곱측도로 묶는 과정을 정리한다. 독립성이 P_(X,Y)=P_X⊗P_Y라는 측도 하나의 등식으로 환원됨을 보이고, 음이 아닌 함수의 Tonelli와 절대적분가능성을 요구하는 Fubini를 구분한다. 순서 교환이 실제로 값을 바꾸는 반례, pairwise와 mutual independence의 차이, E[XY]=E[X]E[Y]와 밀도의 곱분해가 독립성의 정의가 아니라 귀결임을 확인하고, iid 가정이 empirical risk의 불편성과 1/n 분산 감소를 어떻게 떠받치는지로 마무리한다."
series: "Measure Theory for AI"
series_order: 7
aliases:
  - "/posts/곱측도-fubini-독립성/"
vault_source: "Distillation/Study/Measure Theory for AI/원고/7강. 곱측도, Fubini, 독립성.md"
---

# 들어가는 말: `\(D=(X_1,\dots,X_n)\sim P^n\)`은 정확히 무슨 뜻인가?

머신러닝 논문을 읽다 보면 거의 첫 페이지에서 이런 표기를 만난다.


```math
X_1,\dots,X_n \overset{\mathrm{iid}}{\sim} P
```


또는


```math
D=(X_1,\dots,X_n)\sim P^n.
```


보통 우리는 이것을

> “`\(P\)`라는 데이터 분포에서 샘플을 `\(n\)`개 독립적으로 뽑았다.”

라고 읽는다.

그런데 측도론적으로 보면 이 한 줄에는 지금까지 배운 거의 모든 개념이 들어 있다.

각 `\(X_i\)` 하나의 분포는 3강에서 배운 push-forward 측도


```math
P_{X_i}=P
```


다.

하지만 데이터셋 전체


```math
D=(X_1,\dots,X_n)
```


는 개별 `\(X_i\)`처럼 `\(\mathcal X\)`에 값을 갖는 확률변수가 아니라 정확히는


```math
D:\Omega\to\mathcal X^n
```


인 **`\(\mathcal X^n\)`-값 확률변수**다.

따라서 `\(D\)` 역시 하나의 분포를 갖는다.


```math
P_D=P_{(X_1,\dots,X_n)}.
```


문제는 이것이다.

각 좌표의 분포가 모두 `\(P\)`라는 사실만으로 이 공동분포가 결정될까?

아니다.

예를 들어 `\(X\sim N(0,1)\)`라고 하자. 두 번째 좌표 `\(Y\)`를 잡는 방법을 두 가지만 비교해 보자.

**(a) `\(Y=X\)`로 잡는 경우.**

물론 `\(Y\sim N(0,1)\)`이다. 그런데 `\((X,Y)\)`는 언제나 대각선


```math
\Delta=\{(x,x):x\in\mathbb R\}
```


위에만 놓인다. 즉 공동분포는 `\(x\mapsto(x,x)\)`라는 사상에 의한 `\(N(0,1)\)`의 push-forward이고,


```math
P_{(X,Y)}(\Delta)=1
```


이다. 이 측도는 평면 위의 Lebesgue 측도에 대해 특이(singular)하다. 2차원 밀도 같은 것은 존재하지 않는다.

**(b) `\(Y\)`를 `\(X\)`와 독립인 새 표준정규변수로 잡는 경우.**

역시 `\(Y\sim N(0,1)\)`이다. 하지만 이번에는 `\((X,Y)\)`가 평면 전체에 퍼지고, 공동분포는 밀도


```math
p(x,y)=\frac{1}{2\pi}e^{-(x^2+y^2)/2}
```


를 갖는 `\(N(0,I_2)\)`가 된다.

두 경우의 주변분포는


```math
P_X=P_Y=N(0,1)
```


로 완전히 같다. 그러나 공동분포는 다르다. 

즉


```math
\boxed{\text{주변분포들만 알아서는 공동분포를 알 수 없다.}}
```


그렇다면 “independent”라는 조건이 무엇을 추가하는 것일까?

이번 강의 핵심은 정확히 이 질문에 답하는 것이다.


```math
\boxed{ X_1,\dots,X_n\text{ independent} \quad\Longleftrightarrow\quad P_{(X_1,\dots,X_n)} = P_{X_1}\otimes\cdots\otimes P_{X_n} }
```


따라서


```math
X_1,\dots,X_n\overset{\mathrm{iid}}{\sim}P
```


라는 한 줄은 사실


```math
\boxed{ P_{(X_1,\dots,X_n)} = P^{\otimes n} }
```


이라는 측도론적 문장이다.

여기서 새로 등장한


```math
P^{\otimes n}
```


이 바로 **곱측도(product measure)**다.

그리고 곱측도 위의 적분


```math
\int_{\mathcal X\times\mathcal Y}f(x,y)\, d(P_X\otimes P_Y)(x,y)
```


를 우리가 익숙한


```math
\int_{\mathcal X} \left( \int_{\mathcal Y}f(x,y)\,dP_Y(y) \right)dP_X(x)
```


로 바꾸어 주는 정리가 Tonelli와 Fubini다.

---

# 요약

이번 강의 흐름은 다음과 같다.

### 1. 두 측도공간을 하나로 묶으면 곱공간이 된다

두 측도공간


```math
(\mathcal X,\mathcal A,\mu), \qquad (\mathcal Y,\mathcal B,\nu)
```


에서


```math
\mathcal X\times\mathcal Y
```


를 만들고, 사각형 모양의 사건


```math
A\times B
```


에


```math
(\mu\otimes\nu)(A\times B) = \mu(A)\nu(B)
```


를 주는 측도를 만든다.

이것이 곱측도다.

---

### 2. 공동분포는 곱공간 위의 측도다

확률변수 `\(X,Y\)`가 있으면


```math
(X,Y):\Omega\to\mathcal X\times\mathcal Y
```


라는 하나의 확률변수로 묶을 수 있다.

그 push-forward


```math
P_{(X,Y)}
```


가 공동분포다.

그리고


```math
\boxed{ X\perp Y \iff P_{(X,Y)}=P_X\otimes P_Y }
```


이다.

---

### 3. Tonelli와 Fubini는 곱측도 적분을 반복적분으로 바꾼다

`\(\mu,\nu\)`가 `\(\sigma\)`-유한이고 `\(f\ge0\)`이면 Tonelli:


```math
\boxed{ \int f\,d(\mu\otimes\nu) = \int\left(\int f(x,y)\,d\nu(y)\right)d\mu(x) = \int\left(\int f(x,y)\,d\mu(x)\right)d\nu(y) }
```


값이 `\(+\infty\)`여도 괜찮다.

부호가 있는 `\(f\)`에 대해서는


```math
\int |f|\,d(\mu\otimes\nu)<\infty
```


라는 조건 아래 Fubini를 쓴다.

---

### 4. iid는 독립 + 동일분포다


```math
X_1,\dots,X_n\overset{\mathrm{iid}}{\sim}P
```


는


```math
P_{X_i}=P
```


이면서


```math
P_{(X_1,\dots,X_n)} = P^{\otimes n}
```


이라는 뜻이다.

즉 데이터셋 하나는 `\(\mathcal X^n\)` 위의 하나의 샘플이다.

---

### 5. 독립이면 기댓값과 밀도가 분해된다

적절한 적분가능성 아래


```math
\boxed{ E[XY]=E[X]E[Y]. }
```


또 `\(X,Y\)`가 각각 어떤 기준측도에 대한 밀도 `\(p_X,p_Y\)`를 가지고 독립이라면


```math
\boxed{ p_{X,Y}(x,y)=p_X(x)p_Y(y) }
```


가 된다.


---

# 1. 두 측도공간을 하나로 묶는다

두 측도공간이 있다고 하자.


```math
(\mathcal X,\mathcal A,\mu), \qquad (\mathcal Y,\mathcal B,\nu).
```


예를 들어


```math
\mathcal X=\mathcal Y=\mathbb R
```


라면 두 실수값 변수 `\(x,y\)`를 동시에 다루기 위해 자연스럽게


```math
\mathbb R^2=\mathbb R\times\mathbb R
```


를 생각하게 된다.

집합 자체를 만드는 것은 어렵지 않다.

문제는 그 위에 어떤 `\(\sigma\)`-대수를 올리고 어떤 측도를 줄 것인가다.

---

## 먼저 사각형 사건부터 보자

`\(A\in\mathcal A\)`, `\(B\in\mathcal B\)`에 대해


```math
A\times B = \{(x,y):x\in A,\ y\in B\}
```


를 생각하자.

확률론적으로 보면 이것은

> “`\(x\)`가 `\(A\)`에 들어가고 동시에 `\(y\)`가 `\(B\)`에 들어간다.”

라는 사건이다.

두 축이 서로 독립적으로 움직이는 측도를 만들고 싶다면 가장 자연스러운 정의는


```math
\boxed{ (\mu\otimes\nu)(A\times B) = \mu(A)\nu(B) }
```


다.

예를 들어 `\([0,1]^2\)`의 Lebesgue 측도라면


```math
\lambda^2(A\times B) = \lambda(A)\lambda(B)
```


이고, 이것은 우리가 초등학교 때부터 알고 있던


```math
\text{직사각형의 넓이} = \text{가로 길이}\times\text{세로 길이}
```


와 정확히 같은 구조다.

곱측도는 이 아이디어를 일반적인 측도공간으로 옮긴 것이다.

---

# 2. 곱 `\(\sigma\)`-대수

하지만 `\(A\times B\)` 꼴의 집합만으로는 부족하다.

확률변수를 다루려면 `\(\sigma\)`-대수가 필요하다.

그래서 모든 measurable rectangle


```math
A\times B, \qquad A\in\mathcal A,\ B\in\mathcal B
```


을 포함하는 가장 작은 `\(\sigma\)`-대수를 만든다.


```math
\boxed{ \mathcal A\otimes\mathcal B := \sigma \left( \{A\times B:A\in\mathcal A,\ B\in\mathcal B\} \right) }
```


이를 **곱 `\(\sigma\)`-대수(product `\(\sigma\)`-algebra)**라고 한다.

따라서 두 측도공간을 합친 공간은


```math
\boxed{ (\mathcal X\times\mathcal Y,\, \mathcal A\otimes\mathcal B) }
```


가 된다.

여기서 한 가지 익숙한 예를 확인해 보자.


```math
\mathcal X=\mathbb R^m,\qquad \mathcal Y=\mathbb R^n
```


이고 각각 Borel `\(\sigma\)`-대수를 쓰면


```math
\mathcal B(\mathbb R^m) \otimes \mathcal B(\mathbb R^n) = \mathcal B(\mathbb R^{m+n}).
```


즉 우리가 평소 아무 생각 없이 쓰던


```math
(X,Y)\in\mathbb R^{m+n}
```


의 measurable structure가 바로 이 곱 `\(\sigma\)`-대수다.

---

## 곁가지: 왜 곱 `\(\sigma\)`-대수인가

집합 `\(\mathcal X\times\mathcal Y\)`에는 `\(\sigma\)`-대수가 저절로 딸려오지 않는다. `\(\mathcal A\)`와 `\(\mathcal B\)`는 각각 `\(\mathcal X\)`, `\(\mathcal Y\)` 위의 것이기 때문이다. `\(\sigma\)`-대수의 공리만 따지면 후보는 많다. 가장 큰 것은 모든 부분집합을 모은 멱집합 `\(\mathcal P(\mathcal X\times\mathcal Y)\)`이고, 가장 작은 것은 `\(\{\emptyset,\mathcal X\times\mathcal Y\}\)`다. 2강에서 `\(\mathbb R\)`의 멱집합을 쓰지 못한 것은 그 위에 길이를 줄 수 없어서였지, 멱집합이 `\(\sigma\)`-대수가 아니어서가 아니었다. 모든 후보는 이 두 극단 사이에 있고, 문제는 그중 무엇을 고르느냐다.

데이터셋 `\(D\)`를 “`\(\mathcal X^n\)`-값 확률변수”라고 부른 순간, 곱공간의 `\(\sigma\)`-대수에 이미 두 가지를 요구한 셈이다. 
좌표가 두 개인 경우로 보자. 곱공간 위의 `\(\sigma\)`-대수 후보를 `\(\mathcal E\)`라 하고, 좌표 사영을 `\(\pi_1(x,y)=x\)`, `\(\pi_2(x,y)=y\)`라 하자.

**요구 1. 각 좌표를 읽을 수 있어야 한다.**

공동분포에서 각 변수의 분포(4절의 주변분포)를 꺼내려면 `\(\pi_1,\pi_2\)`가 가측이어야 한다. 그런데


```math
\pi_1^{-1}(A)\cap\pi_2^{-1}(B)=(A\times\mathcal Y)\cap(\mathcal X\times B)=A\times B
```


이므로 두 사영이 가측이면 모든 rectangle이 `\(\mathcal E\)`에 들어가고, 따라서 `\(\mathcal E\)`는 rectangle을 담는 가장 작은 `\(\sigma\)`-대수인 `\(\mathcal A\otimes\mathcal B\)`를 포함한다. 반대 방향은 `\(\pi_1^{-1}(A)\)`와 `\(\pi_2^{-1}(B)\)` 자체가 rectangle이라는 데서 바로 나온다.


```math
\boxed{ \text{요구 1} \iff \mathcal E\supseteq\mathcal A\otimes\mathcal B }
```


**요구 2. 확률변수를 묶어도 확률변수여야 한다.**

어떤 확률공간 위에서든 `\(X:\Omega\to\mathcal X\)`와 `\(Y:\Omega\to\mathcal Y\)`가 확률변수이면 `\((X,Y):\Omega\to\mathcal X\times\mathcal Y\)`도 확률변수여야 한다. `\(D=(X_1,\dots,X_n)\)`을 하나의 확률변수로 부를 수 있는 근거가 이것이다.

곱 `\(\sigma\)`-대수는 이 요구를 만족한다. 생성원인 rectangle에서


```math
(X,Y)^{-1}(A\times B)=X^{-1}(A)\cap Y^{-1}(B)\in\mathcal F
```


이고, 3강 5절에서 본 대로 가측성은 생성원에서만 확인하면 되기 때문이다. 

반대로 요구 2는 `\(\mathcal E\)`가 곱 `\(\sigma\)`-대수보다 커지는 것을 막는다. 표본공간을 곱공간 자체로 잡아 보자.


```math
\Omega=\mathcal X\times\mathcal Y,\qquad \mathcal F=\mathcal A\otimes\mathcal B,\qquad X=\pi_1,\qquad Y=\pi_2
```


가측성은 측도와 무관하므로 확률측도는 아무것이나 올려 두면 된다. 요구 1에서 본 대로 `\(\pi_1,\pi_2\)`는 `\(\mathcal A\otimes\mathcal B\)`에 대해 가측이니 `\(X,Y\)`는 확률변수다. 그런데 `\((X,Y)(x,y)=(x,y)\)`, 즉 `\((X,Y)\)`는 항등사상이다. 요구 2에 따라 이것이 `\(\mathcal E\)`에 대해 가측이어야 하므로 모든 `\(E\in\mathcal E\)`에 대해


```math
E=(X,Y)^{-1}(E)\in\mathcal F=\mathcal A\otimes\mathcal B.
```


즉


```math
\boxed{ \text{요구 2} \Longrightarrow \mathcal E\subseteq\mathcal A\otimes\mathcal B }
```


다. 표본공간을 곱공간으로 잡고 좌표 사영을 확률변수로 쓰는 이 구성은 13절에서 iid 데이터셋을 만들 때 다시 나온다.

두 요구를 합치면 답이 나온다.


```math
\boxed{ \text{좌표를 읽을 수 있고 묶어도 확률변수가 되는 }\sigma\text{-대수는 }\mathcal A\otimes\mathcal B\text{ 하나뿐이다.} }
```


곱 `\(\sigma\)`-대수를 다 담지 못하면 좌표를 읽을 수 없고, 곱 `\(\sigma\)`-대수 밖의 집합을 하나라도 담으면 확률변수 두 개를 묶은 것이 확률변수가 아닐 수 있다. 

측도는 사정이 다르다. 두 좌표의 분포를 모두 정해 줘도 곱공간 위의 측도는 하나로 정해지지 않는다. 들어가는 말의 (a)와 (b)는 같은 `\(\mathcal B(\mathbb R^2)\)` 위에서 주변분포까지 같은데도 서로 다른 측도였다. 이 이야기는 6절의 coupling에서 이어진다.


---

# 3. 곱측도는 어떻게 만들어지는가

이제


```math
A\times B
```


에 대해


```math
\mu(A)\nu(B)
```


라는 값을 주고 싶다.

문제는 이 규칙을


```math
\mathcal A\otimes\mathcal B
```


전체로 어떻게 확장하느냐다.

여기서 2강에서 봤던 Carathéodory 확장정리가 다시 등장한다.

대략적인 구조는


```math
\boxed{ \text{rectangle} \longrightarrow \text{rectangle들의 유한 서로소 합집합으로 이루어진 대수} \longrightarrow \text{Carathéodory 확장} }
```


이다.

결과만 가져가자.

`\(\mu,\nu\)`가 **`\(\sigma\)`-유한**(`\(\sigma\)`-finite)이면


```math
\boxed{ (\mu\otimes\nu)(A\times B) = \mu(A)\nu(B) }
```


를 만족하는 곱측도


```math
\mu\otimes\nu
```


가 존재하고 유일하다.

`\(\sigma\)`-유한이란 공간 전체를 가산 개의 조각 `\(E_1,E_2,\dots\)`로 덮되, 각 조각의 측도가 유한하게 할 수 있다는 뜻이다. 즉 `\(\mathcal X=\bigcup_n E_n\)`이고 모든 `\(n\)`에 대해 `\(\mu(E_n)<\infty\)`이다. 확률측도처럼 유한한 측도는 당연히 `\(\sigma\)`-유한이고, `\(\mathbb R^d\)` 위의 Lebesgue 측도(상자 `\([-k,k]^d\)`로 덮는다)와 `\(\mathbb N\)` 위의 counting measure(한 점씩 덮는다)도 `\(\sigma\)`-유한이다.

따라서


```math
(\mathcal X,\mathcal A,\mu), \qquad (\mathcal Y,\mathcal B,\nu)
```


로부터


```math
\boxed{ (\mathcal X\times\mathcal Y,\, \mathcal A\otimes\mathcal B,\, \mu\otimes\nu) }
```


라는 새로운 측도공간을 얻는다.

이번 강에서 곱측도의 구성 자체를 증명하지는 않는다.

중요한 것은 그 의미다.


```math
\boxed{ \mu\otimes\nu = \text{두 좌표가 서로 독립적으로 움직이는 측도} }
```


라고 생각하면 된다.

---

# 4. 공동분포는 곱공간 위의 측도다

3강에서 확률변수 `\(X\)`의 분포를


```math
P_X=P\circ X^{-1}
```


라는 push-forward 측도로 정의했다.

이제 확률변수가 두 개 있다고 하자.


```math
X:\Omega\to\mathcal X, \qquad Y:\Omega\to\mathcal Y.
```


둘을 하나로 묶으면


```math
(X,Y):\Omega\to\mathcal X\times\mathcal Y
```


라는 새로운 확률변수가 된다. 곱공간에 곱 `\(\sigma\)`-대수를 준 덕분이다.

따라서 3강의 정의를 그대로 적용해


```math
\boxed{ P_{(X,Y)} = P\circ(X,Y)^{-1} }
```


를 정의할 수 있다.

이것이 `\(X,Y\)`의 **공동분포(joint distribution)**다.

정의역까지 적으면


```math
P_{(X,Y)}:\mathcal A\otimes\mathcal B\to[0,1],\qquad E\mapsto P\big((X,Y)^{-1}(E)\big)
```


이다. 즉 공동분포는 `\((\mathcal X\times\mathcal Y,\,\mathcal A\otimes\mathcal B)\)` 위의 확률측도다. 이름이 비슷하지만 곱측도와는 다르다. 곱 `\(\sigma\)`-대수 위의 확률측도는 무수히 많고 곱측도 `\(P_X\otimes P_Y\)`는 그중 하나일 뿐이다. 공동분포가 바로 그 하나가 되는 경우가 5절의 독립이다.

즉


```math
\boxed{ \text{공동분포} = \text{곱공간 위의 push-forward 측도} }
```


다.

---

## 주변분포는 공동분포의 그림자다

공동분포 `\(P_{(X,Y)}\)`를 알고 있다면 각각의 분포는 다시 얻을 수 있다.

예를 들어 `\(A\in\mathcal A\)`에 대해


```math
P_X(A) = P_{(X,Y)}(A\times\mathcal Y).
```


마찬가지로


```math
P_Y(B) = P_{(X,Y)}(\mathcal X\times B).
```


이를 주변분포(marginal distribution)라고 한다.

그림으로 생각하면 공동분포가 2차원의 물체이고 주변분포는 각 축으로 투영한 그림자다.


```math
\boxed{ P_{(X,Y)} \longrightarrow P_X,\ P_Y }
```


는 가능하다.

하지만 역방향은 일반적으로 불가능하다.


```math
P_X,\ P_Y
```


만으로 `\(P_{(X,Y)}\)`를 복원할 수는 없다.

두 변수가 어떻게 **의존(depend)**하는지에 대한 정보가 사라졌기 때문이다.

---

# 5. 독립성이 채워 주는 정보

사건 `\(A,B\)`의 독립은 익숙하다.


```math
\boxed{ P(A\cap B)=P(A)P(B). }
```


이제 확률변수로 올라가 보자.

`\(X,Y\)`가 독립이라는 것은 모든 measurable set


```math
A\in\mathcal A,\qquad B\in\mathcal B
```


에 대해


```math
P(X\in A,\ Y\in B) = P(X\in A)P(Y\in B)
```


가 성립한다는 뜻이다.

왼쪽을 공동분포로 쓰면


```math
P_{(X,Y)}(A\times B)
```


이고 오른쪽은


```math
P_X(A)P_Y(B).
```


그런데 곱측도의 정의가


```math
(P_X\otimes P_Y)(A\times B) = P_X(A)P_Y(B)
```


였다.

따라서 독립이면 모든 measurable rectangle에서


```math
P_{(X,Y)}(A\times B) = (P_X\otimes P_Y)(A\times B).
```


그리고 두 확률측도가 이 rectangle들에서 값이 같으면 전체 곱 `\(\sigma\)`-대수에서도 같아진다.

rectangle들의 모임은


```math
(A\times B)\cap(A'\times B') = (A\cap A')\times(B\cap B')
```


이므로 교집합에 닫힌 π-체계이고, 곱 `\(\sigma\)`-대수를 생성한다. 그래서 3강 11절에서 본 π-λ 정리를 그대로 쓸 수 있다.

결국


```math
\boxed{ X\perp Y \iff P_{(X,Y)} = P_X\otimes P_Y }
```


를 얻는다.

이 식이 이번 강에서 가장 중요한 식이다.

독립성이 더 이상


```math
P(A\cap B)=P(A)P(B)
```


라는 여러 개의 확률 계산 규칙이 아니다.

측도 하나에 대한 구조적 명제가 된다.


```math
\boxed{ \text{독립} = \text{공동분포가 주변분포들의 곱측도이다.} }
```


---

# 6. 여기서 중요한 함정 하나

다음 식을 자주 본다.


```math
E[f(X,Y)] = \int_{\mathcal X} \int_{\mathcal Y} f(x,y)\,dP_Y(y)dP_X(x).
```


이것은 **항상 참이 아니다.**

일반적인 `\(X,Y\)`에 대해 항상 참인 식은


```math
\boxed{ E[f(X,Y)] = \int_{\mathcal X\times\mathcal Y} f(x,y)\,dP_{(X,Y)}(x,y) }
```


이다.

5강 LOTUS를 벡터값 확률변수 `\((X,Y)\)`에 적용했을 뿐이다.

만약 `\(X,Y\)`가 독립이라면


```math
P_{(X,Y)}=P_X\otimes P_Y
```


이므로 비로소


```math
E[f(X,Y)] = \int f\,d(P_X\otimes P_Y)
```


가 된다.

그리고 여기서 Tonelli 또는 Fubini를 사용하면


```math
E[f(X,Y)] = \int_{\mathcal X} \left[ \int_{\mathcal Y} f(x,y)\,dP_Y(y) \right]dP_X(x)
```


로 바꿀 수 있다.

즉


```math
\boxed{ \text{독립성} \quad+\quad \text{Tonelli/Fubini} }
```


가 결합되어 우리가 익숙한


```math
E_XE_Y[f(X,Y)]
```


표현을 만들어 낸다.

반대로 `\(X,Y\)`가 의존하고 있는데


```math
\int\int f(x,y)\,dP_X(x)dP_Y(y)
```


를 계산하면, 그것은 원래의 공동분포가 아니라


```math
P_X\otimes P_Y
```


라는 **독립 coupling** 아래에서의 기댓값을 계산하는 셈이다.

---

## 곁가지: coupling이라는 말

“독립 coupling”이라는 표현을 썼으니 여기서 한 번 정리하고 가자.

확률론에서 **coupling**은 *주변분포를 고정한 채 공동분포를 하나 고르는 일*, 그리고 *그렇게 골라진 공동분포*를 뜻한다. 어원 그대로 두 확률변수를 하나의 확률공간 위에 함께 묶는다(couple)는 뜻이다.

`\(\mu\)`가 `\(\mathcal X\)` 위의, `\(\nu\)`가 `\(\mathcal Y\)` 위의 확률측도일 때


```math
\boxed{ \Pi(\mu,\nu)=\big\{\ \pi\ \text{on}\ \mathcal X\times\mathcal Y\ :\ (\pi_1)_{\#}\pi=\mu,\ \ (\pi_2)_{\#}\pi=\nu\ \big\} }
```


를 `\(\mu,\nu\)`의 **coupling들의 집합**이라 한다. `\(\pi_1,\pi_2\)`는 좌표 사영이고, `\((\cdot)_{\#}\)`는 push-forward 기호다([3강. 가측함수, 확률변수, 분포와 Push-forward](/posts/measure-theory-for-ai/가측함수-확률변수-분포와-push-forward/) 9절).

`\(\Pi(\mu,\nu)\)`는 *`\(\mathcal X\times\mathcal Y\)` 위의 확률측도 중 두 좌표사영에 의한 주변분포가 각각 `\(\mu\)`와 `\(\nu\)`인 것들을 전부 모은 집합*이다.

4절의 “주변분포는 공동분포의 그림자다”를 뒤집어 놓은 것이 이 집합이다. 그림자를 먼저 고정해 놓고, 그 그림자를 갖는 본체를 전부 모은 것이다.

그러면 이 강의가 처음부터 반복해 온 관찰은 한 줄로 요약된다.

> `\(\Pi(\mu,\nu)\)`의 원소는 하나가 아니다.

그리고 곱측도는 그 안의 원소 **하나**일 뿐이다.


```math
\mu\otimes\nu\ \in\ \Pi(\mu,\nu)
```


이 원소를 **독립 coupling**(independent coupling)이라 부른다. 언제나 만들 수 있으므로 `\(\Pi(\mu,\nu)\neq\emptyset\)`을 보장하는 역할도 한다.

예시를 통해 확인해 보자. `\(X\sim\mathrm{Bernoulli}(1/2)\)`이고 `\(Y=X\)`라 하자.

| 점 | 진짜 `\(P_{(X,Y)}\)` | 독립 coupling `\(P_X\otimes P_Y\)` |
|---|---|---|
| `\((0,0)\)` | `\(1/2\)` | `\(1/4\)` |
| `\((0,1)\)` | `\(0\)` | `\(1/4\)` |
| `\((1,0)\)` | `\(0\)` | `\(1/4\)` |
| `\((1,1)\)` | `\(1/2\)` | `\(1/4\)` |

두 측도의 **주변분포는 완전히 같다.** 둘 다 각 좌표에서 `\(\mathrm{Bernoulli}(1/2)\)`다. 그런데 `\(f(x,y)=\mathbf 1\{x=y\}\)`를 넣으면


```math
E_{P_{(X,Y)}}[f]=1, \qquad E_{P_X\otimes P_Y}[f]=\frac12
```


로 값이 갈린다.

의존하는 `\(X,Y\)`에 대해 `\(\int\int f\,dP_X dP_Y\)`를 계산하는 것은 `\(\Pi(P_X,P_Y)\)`의 한 원소인 곱측도에서의 기댓값이다. 그런데 `\(X,Y\)`가 의존하므로 그 원소는 우리가 원했던 `\(P_{(X,Y)}\)`가 아니다. 

`\(\Pi(\mu,\nu)\)`의 다른 원소들에도 이름이 있다. `\(\mu,\nu\)`가 실수 위의 분포일 때 하나의 `\(U\sim\mathrm{Unif}(0,1)\)`로 같은 분위수끼리 묶는 comonotone coupling `\(\big(F_\mu^{-1}(U),F_\nu^{-1}(U)\big)\)`(3강 14절 역변환 샘플링을 같은 `\(U\)`로 두 번 쓴 것이다), 수송비용 `\(\int c\,d\pi\)`를 최소화하는 optimal coupling 등이다. 


---

# 7. Tonelli 정리 — 음이 아니면 먼저 적분해도 된다

이제 곱측도 위의 적분을 반복적분으로 바꿔 보자.

3절에서 본 대로 두 `\(\sigma\)`-유한 측도공간


```math
(\mathcal X,\mathcal A,\mu), \qquad (\mathcal Y,\mathcal B,\nu)
```


와 measurable 함수


```math
f:\mathcal X\times\mathcal Y\to[0,\infty]
```


를 생각하자.

즉


```math
f(x,y)\ge0.
```


그러면 Tonelli 정리는


```math
\boxed{ \int_{\mathcal X\times\mathcal Y} f\,d(\mu\otimes\nu) = \int_{\mathcal X} \left( \int_{\mathcal Y} f(x,y)\,d\nu(y) \right)d\mu(x) }
```


이며 동시에


```math
\boxed{ = \int_{\mathcal Y} \left( \int_{\mathcal X} f(x,y)\,d\mu(x) \right)d\nu(y). }
```


즉


```math
\boxed{ \int\int f(x,y)\,d\nu(y)d\mu(x) = \int\int f(x,y)\,d\mu(x)d\nu(y). }
```


중요한 점은


```math
f\ge0
```


이면 적분값이 `\(+\infty\)`라도 괜찮다는 것이다.

예를 들어


```math
\int f\,d(\mu\otimes\nu)=+\infty
```


여도 식은 여전히 extended real number의 의미에서 성립한다.


```math
\boxed{ \text{Tonelli: nonnegative면 계산해도 된다.} }
```


## `\(\sigma\)`-유한 조건은 장식이 아니다

이 조건을 빼면 `\(f\ge0\)`이어도 Tonelli의 결론이 깨진다.

`\([0,1]\)` 위의 Lebesgue 측도 `\(\lambda\)`와, 같은 `\([0,1]\)` 위의 counting measure `\(\nu\)`를 잡고


```math
f(x,y)=\mathbf 1\{x=y\}
```


를 넣어 보자.

`\(y\)`부터 적분하면 각 `\(x\)`마다 `\(y=x\)`인 점 하나만 세어지므로


```math
\int_{[0,1]}\left(\int_{[0,1]} f(x,y)\,d\nu(y)\right)d\lambda(x) = \int_{[0,1]} 1\,d\lambda = 1.
```


`\(x\)`부터 적분하면 한 점의 Lebesgue 측도는 `\(0\)`이므로


```math
\int_{[0,1]}\left(\int_{[0,1]} f(x,y)\,d\lambda(x)\right)d\nu(y) = \int_{[0,1]} 0\,d\nu = 0.
```


`\(f\ge0\)`인데도 두 반복적분이 다르다. `\([0,1]\)`은 비가산 집합이라 그 위의 counting measure는 측도가 유한한 조각 가산 개로 덮을 수 없다. 즉 `\(\nu\)`가 `\(\sigma\)`-유한이 아니다.

확률측도, Lebesgue 측도, 가산집합 위의 counting measure는 모두 `\(\sigma\)`-유한이므로 ML에서 이 조건에 걸릴 일은 드물다.

---

# 8. Fubini 정리 — 부호가 있으면 절대적분가능성을 확인한다

이번에는 같은 `\(\sigma\)`-유한 측도공간 위에서 `\(f\)`가 양수와 음수를 모두 가질 수 있다고 하자.

이때는 상황이 달라진다.

4강에서 봤듯이


```math
\infty-\infty
```


를 피해야 한다.

따라서 먼저


```math
\boxed{ \int_{\mathcal X\times\mathcal Y} |f(x,y)|\,d(\mu\otimes\nu)<\infty }
```


를 요구한다.

즉


```math
f\in L^1(\mu\otimes\nu).
```


그러면 Fubini 정리에 의해


```math
\boxed{ \int f\,d(\mu\otimes\nu) = \int \left( \int f(x,y)\,d\nu(y) \right)d\mu(x) }
```


이며


```math
\boxed{ = \int \left( \int f(x,y)\,d\mu(x) \right)d\nu(y). }
```


따라서 적분 순서를 자유롭게 바꿀 수 있다.

---

## Tonelli와 Fubini를 어떻게 구분하면 되는가

실전에서는 다음 순서가 가장 안전하다.


```math
\boxed{ \text{1. }|f|\ge0\text{에 Tonelli를 적용한다.} }
```


즉


```math
\int |f|\,d(\mu\otimes\nu)
```


를 반복적분으로 계산한다.

그 결과가 유한하면


```math
\boxed{ f\in L^1(\mu\otimes\nu) }
```


이므로


```math
\boxed{ \text{2. Fubini로 }f\text{의 적분 순서를 바꾼다.} }
```


기억하면


```math
\boxed{ \text{Tonelli로 }|f|\text{를 검사} \quad\Longrightarrow\quad \text{유한하면 Fubini} }
```


다.

---

# 9. 조건을 확인하지 않으면 정말 값이 달라질 수 있다

적분 순서가 왜 이렇게 까다로운지 간단한 이산 예를 보자.

`\(\mathbb N\times\mathbb N\)` 위에 counting measure를 놓고


```math
f(m,n) = \begin{cases} 1, & m=n, \\ -1, & m=n+1, \\ 0, & \text{otherwise} \end{cases}
```


라고 하자.

먼저 `\(n\)`에 대해 더하자.

`\(m=1\)`일 때는


```math
\sum_{n=1}^\infty f(1,n)=1
```


이고, `\(m\ge2\)`이면 `\(+1\)` 하나와 `\(-1\)` 하나가 있어


```math
\sum_{n=1}^\infty f(m,n)=0.
```


따라서


```math
\sum_{m=1}^\infty \left( \sum_{n=1}^\infty f(m,n) \right) = 1.
```


반대로 `\(m\)`에 대해 먼저 더하면 모든 `\(n\)`에 대해


```math
\sum_{m=1}^\infty f(m,n)=1-1=0.
```


따라서


```math
\sum_{n=1}^\infty \left( \sum_{m=1}^\infty f(m,n) \right) = 0.
```


즉


```math
\boxed{ 1\neq0. }
```


무슨 일이 벌어진 것일까?

절댓값을 더해 보면


```math
\sum_{m,n}|f(m,n)|=\infty.
```


즉


```math
f\notin L^1.
```


Fubini의 조건이 깨져 있었다.

`\(\mathbb N\)` 위의 counting measure는 `\(\sigma\)`-유한이므로, 7절의 반례와 달리 여기서 깨진 것은 `\(\sigma\)`-유한 조건이 아니라 적분가능성이다.

그래서 두 반복적분의 값이 달라져도 정리와 모순되지 않는다.

무한합도 counting measure에 대한 적분이므로 이것은 이중적분의 순서를 함부로 바꿀 수 없는 이유를 보여준다.


---

# 10. 사건의 독립에서 `\(\sigma\)`-대수의 독립으로

이제 독립성을 조금 더 일반화하자.

두 사건 `\(A,B\)`의 독립은


```math
P(A\cap B)=P(A)P(B).
```


그런데 확률변수 하나는 단 하나의 사건이 아니라 수많은 사건을 만들어 낸다.

예를 들어 `\(X\)`는


```math
\{X\le1\}, \qquad \{0<X<2\}, \qquad \{X\in A\}
```


같은 모든 사건을 만든다.

이 사건들을 모은 것이


```math
\sigma(X)
```


다.

따라서 “확률변수 `\(X\)`와 `\(Y\)`가 독립이다”라는 것은 사실


```math
\sigma(X)
```


와


```math
\sigma(Y)
```


가 독립이라는 뜻으로 읽는 것이 가장 자연스럽다.

두 `\(\sigma\)`-대수


```math
\mathcal G,\mathcal H\subset\mathcal F
```


가 독립이라는 것은 모든


```math
G\in\mathcal G,\qquad H\in\mathcal H
```


에 대해


```math
\boxed{ P(G\cap H)=P(G)P(H) }
```


가 성립한다는 뜻이다.

그리고


```math
\boxed{ X\perp Y \iff \sigma(X)\perp\sigma(Y). }
```


따라서 독립성은 단순히 두 숫자가 관련이 없다는 뜻이 아니다.


```math
\boxed{ X\text{가 알려 주는 모든 사건} }
```


과


```math
\boxed{ Y\text{가 알려 주는 모든 사건} }
```


사이에 확률적 연관이 없다는 뜻이다.

---

# 11. 세 개 이상에서는 왜 모든 유한 부분족을 확인해야 하는가

확률변수 `\(X_1,X_2,\dots\)`의 독립성을 정의할 때는 단순히 모든 쌍이 독립이라고 하지 않는다.

서로 다른 유한 개의 index


```math
i_1,\dots,i_k
```


와 사건


```math
A_j\in\sigma(X_{i_j})
```


에 대해


```math
\boxed{ P(A_1\cap\cdots\cap A_k) = \prod_{j=1}^kP(A_j) }
```


가 성립해야 한다.

왜 이런 조건이 필요할까?

**pairwise independent와 mutually independent가 다르기 때문이다.**

---

## 쌍마다 독립인데 셋은 독립이 아닌 예

표본공간을


```math
\Omega=\{00,01,10,11\}
```


로 하고 네 점에 각각 확률 `\(1/4\)`를 주자.

사건


```math
A=\{\text{첫 번째 bit가 }0\}, \qquad B=\{\text{두 번째 bit가 }0\}, \qquad C=\{\text{두 bit가 같다}\}
```


를 정의하자.

각각


```math
P(A)=P(B)=P(C)=\frac12.
```


또


```math
P(A\cap B) = P(A\cap C) = P(B\cap C) = \frac14 = \frac12\cdot\frac12.
```


따라서 세 사건은 **쌍마다 독립**이다.

그런데


```math
A\cap B\cap C=\{00\}
```


이므로


```math
P(A\cap B\cap C)=\frac14.
```


완전한 독립이라면


```math
P(A)P(B)P(C) = \frac18
```


이어야 한다.

하지만


```math
\frac14\neq\frac18.
```


따라서


```math
\boxed{ \text{pairwise independence} \not\Rightarrow \text{mutual independence}. }
```


그래서 여러 확률변수의 독립은 모든 유한 부분족에 대해 정의한다.

---

# 12. 여러 확률변수의 독립 = 공동분포의 곱분해

두 변수에서 얻었던


```math
P_{(X,Y)} = P_X\otimes P_Y
```


는 그대로 일반화된다.

확률변수


```math
X_1,\dots,X_n
```


이 독립이라는 것은


```math
\boxed{ P_{(X_1,\dots,X_n)} = P_{X_1}\otimes\cdots\otimes P_{X_n} }
```


와 동치다.

이제 iid의 정확한 의미가 보인다.

`\(X_1,\dots,X_n\)`이 identically distributed라는 것은


```math
P_{X_1} = \cdots = P_{X_n} = P
```


이라는 뜻이다.

independent라는 것은


```math
P_{(X_1,\dots,X_n)} = P_{X_1}\otimes\cdots\otimes P_{X_n}
```


이라는 뜻이다.

둘을 합치면


```math
\boxed{ X_1,\dots,X_n\overset{\mathrm{iid}}{\sim}P \iff P_{(X_1,\dots,X_n)} = P^{\otimes n}. }
```


보통 `\(P^{\otimes n}\)`을 간단히 `\(P^n\)`이라고 쓰기도 한다.

따라서 머신러닝에서


```math
D=(X_1,\dots,X_n)\sim P^n
```


이라고 쓸 때 실제 의미는


```math
\boxed{ D\text{라는 }\mathcal X^n\text{-값 확률변수의 분포가 }P^{\otimes n}\text{이다.} }
```


라는 것이다.

---

# 13. iid 데이터셋을 곱공간 자체에서 만들 수도 있다

더 재미있는 관점도 있다.

먼저 하나의 데이터 분포


```math
(\mathcal X,\mathcal A,P)
```


만 주어졌다고 하자.

표본공간 자체를


```math
\Omega=\mathcal X^n
```


으로 잡고


```math
\mathcal F=\mathcal A^{\otimes n}, \qquad \mathbb P=P^{\otimes n}
```


로 놓는다.

그리고 좌표사상


```math
X_i(x_1,\dots,x_n)=x_i
```


를 정의하자.

그러면 자동으로


```math
X_i\sim P
```


이고


```math
X_1,\dots,X_n
```


은 독립이다.

즉


```math
\boxed{ (\mathcal X^n,\mathcal A^{\otimes n},P^{\otimes n}) }
```


라는 확률공간 하나만 만들면 그 위에 iid sample들이 자연스럽게 존재한다.

무한 수열도 마찬가지다.

적절한 무한곱 측도를 이용해


```math
\Omega=\mathcal X^{\mathbb N}
```


위에


```math
P^{\otimes\mathbb N}
```


을 만들고


```math
X_i(\omega)=\omega_i
```


라는 좌표사상을 취하면


```math
X_1,X_2,\dots\overset{\mathrm{iid}}{\sim}P
```


인 무한 iid 수열을 얻을 수 있다.

이번 강에서는 무한곱 측도의 구성을 증명하지 않는다.

다만 기억해 둘 것은


```math
\boxed{ \text{"iid 수열을 하나 잡자"는 말 자체가 수학적으로 정당화될 수 있다.} }
```


는 것이다.

---

# 14. 독립이면 기댓값이 곱으로 분해된다

이제 가장 익숙한 결과를 측도론적으로 다시 보자.

`\(X,Y\)`가 독립이고


```math
E[|X|]<\infty, \qquad E[|Y|]<\infty
```


라고 하자.

독립이므로


```math
P_{(X,Y)} = P_X\otimes P_Y.
```


따라서


```math
E[XY] = \int xy\,d(P_X\otimes P_Y)(x,y).
```


먼저 절댓값을 보면 Tonelli에 의해


```math
\begin{aligned} E[|XY|] &= \int |xy|\,d(P_X\otimes P_Y)\\ &= \int |x| \left( \int |y|\,dP_Y(y) \right)dP_X(x)\\ &= E[|X|]E[|Y|] <\infty. \end{aligned}
```


따라서 `\(XY\in L^1\)`이고 Fubini를 사용할 수 있다.


```math
\begin{aligned} E[XY] &= \int x \left( \int y\,dP_Y(y) \right)dP_X(x)\\ &= \int xE[Y]\,dP_X(x)\\ &= E[X]E[Y]. \end{aligned}
```


즉


```math
\boxed{ X\perp Y,\quad X,Y\in L^1 \quad\Longrightarrow\quad E[XY]=E[X]E[Y]. }
```


이 식은 독립성의 정의가 아니라 독립성으로부터 Tonelli/Fubini를 통해 나오는 결과다.

---

# 15. 독립이면 공분산은 0이다 — 하지만 역은 아니다

6강에서 본 공분산의 정의


```math
\operatorname{Cov}(X,Y) = E[(X-E[X])(Y-E[Y])]
```


를 전개하면


```math
\operatorname{Cov}(X,Y) = E[XY]-E[X]E[Y]
```


이다.

따라서 `\(X,Y\in L^2\)`이고 독립이면


```math
E[XY]=E[X]E[Y]
```


이므로


```math
\boxed{ X\perp Y \quad\Longrightarrow\quad \operatorname{Cov}(X,Y)=0. }
```


6강의 기하학으로 읽으면 독립인 두 확률변수의 중심화 벡터


```math
X-E[X], \qquad Y-E[Y]
```


는 서로 직교한다.

하지만 역은 일반적으로 거짓이다.


```math
\boxed{ \operatorname{Cov}(X,Y)=0 \not\Rightarrow X\perp Y. }
```


예를 들어


```math
X\sim\operatorname{Unif}[-1,1], \qquad Y=X^2
```


라고 하자.

`\(Y\)`는 `\(X\)`가 정해지면 완전히 결정된다.

다만 함수 관계만으로 독립이 깨지는 것은 아니다. 상수함수 `\(Y=c\)`도 `\(X\)`의 함수지만 `\(X\)`와 독립이다. 독립이 아님을 보이려면 곱셈 규칙이 깨지는 사건을 하나 찾아야 한다.


```math
P\left(|X|\le\tfrac12,\ Y>\tfrac14\right) = 0 \neq \frac14 = P\left(|X|\le\tfrac12\right)P\left(Y>\tfrac14\right).
```


`\(|X|\le\frac12\)`이면 `\(Y=X^2\le\frac14\)`이므로 왼쪽은 `\(0\)`이고, 오른쪽은 `\(\frac12\cdot\frac12\)`다.

그런데 대칭성 때문에


```math
E[X]=0,\qquad E[X^3]=0
```


이고


```math
\operatorname{Cov}(X,X^2) = E[X^3]-E[X]E[X^2] = 0.
```


즉 uncorrelated는 단지 `\(L^2\)`에서 직교한다는 뜻이고, independence는 공동분포 전체가 곱으로 분리된다는 훨씬 강한 조건이다.


```math
\boxed{ \text{independence} \Longrightarrow \text{uncorrelated}, \qquad \text{converse는 일반적으로 거짓}. }
```


---

# 16. iid가 empirical risk의 계산을 단순하게 만드는 이유

머신러닝으로 돌아오자.

데이터


```math
X_1,\dots,X_n\overset{\mathrm{iid}}{\sim}P
```


와 loss


```math
\ell(\theta,X)
```


가 있다고 하자.

population risk는


```math
R(\theta) = E_{X\sim P}[\ell(\theta,X)]
```


이고 empirical risk는


```math
\hat R_n(\theta) = \frac1n \sum_{i=1}^n \ell(\theta,X_i)
```


이다.

동일분포이므로 각 항에 대해


```math
E[\ell(\theta,X_i)] = R(\theta).
```


따라서 기댓값의 선형성만으로


```math
\boxed{ E[\hat R_n(\theta)] = R(\theta). }
```


즉 empirical risk는 population risk의 unbiased estimator다.

여기에 독립성까지 쓰고 loss가 `\(L^2\)`에 있다고 하자.

서로 다른 `\(i\neq j\)`에 대해


```math
\operatorname{Cov} \left( \ell(\theta,X_i), \ell(\theta,X_j) \right) = 0.
```


따라서


```math
\begin{aligned} \operatorname{Var}(\hat R_n) &= \operatorname{Var} \left( \frac1n\sum_{i=1}^n\ell(\theta,X_i) \right)\\ &= \frac1{n^2} \sum_{i=1}^n \operatorname{Var}(\ell(\theta,X_i))\\ &= \frac1n \operatorname{Var}(\ell(\theta,X)). \end{aligned}
```


즉


```math
\boxed{ \operatorname{Var}(\hat R_n) = \frac{\operatorname{Var}(\ell)}{n}. }
```


우리가 샘플 수를 늘리면 Monte Carlo 오차가 줄어든다고 말할 때 그 뒤에는 독립성이 숨어 있다.


```math
\boxed{ \text{iid} \longrightarrow \text{곱측도} \longrightarrow \text{기댓값과 공분산의 분해} \longrightarrow \text{Monte Carlo 평균의 안정화} }
```


라는 구조다.

단 지금까지의 `\(\theta\)`는 데이터와 무관하게 **미리 고정된** 값이다.

데이터로 학습한 `\(\hat\theta=\hat\theta(D)\)`를 넣으면 두 계산 모두 근거를 잃는다. 각 항 `\(\ell(\hat\theta,X_i)\)` 안에 `\(\hat\theta\)`를 통해 데이터셋 전체가 들어가 있어서 항들이 더 이상 독립이 아니고, 불편성도 깨진다.

예를 들어 `\(\hat\theta\)`가 `\(\hat R_n\)`을 최소화하는 값(ERM)이면, 아무 고정된 `\(\theta\)`에 대해서도 `\(\hat R_n(\hat\theta)\le\hat R_n(\theta)\)`이므로 위의 불편성에서 `\(E[\hat R_n(\hat\theta)]\le R(\theta)\)`다. `\(\theta\)`에 대해 하한을 취하면


```math
E[\hat R_n(\hat\theta)] \le \inf_\theta R(\theta) \le E[R(\hat\theta)].
```


오른쪽 부등식은 표본마다 `\(R(\hat\theta)\ge\inf_\theta R(\theta)\)`이기 때문이다.

즉 학습 loss는 평균적으로 실제 risk를 과소평가하고, 그 차이가 generalization gap이다.

---

# 17. 독립이면 공동밀도는 밀도의 곱이다

확률론에서 매우 익숙한 식이 있다.


```math
\boxed{ p_{X,Y}(x,y) = p_X(x)p_Y(y). }
```


보통 이것을 독립성의 정의처럼 외운다.

하지만 측도론적으로 보면 순서가 반대다.

독립성의 근본적인 정의는


```math
\boxed{ P_{(X,Y)} = P_X\otimes P_Y }
```


이다.

이제 추가로 `\(P_X,P_Y\)`가 각각 어떤 `\(\sigma\)`-유한 기준측도 `\(\mu,\nu\)`에 대해 밀도를 가지고 있다고 하자.

즉 어떤 함수 `\(p_X,p_Y\)`가 있어서


```math
P_X(A)=\int_A p_X\,d\mu, \qquad P_Y(B)=\int_B p_Y\,d\nu
```


라고 하자.

독립이면 measurable rectangle `\(A\times B\)`에 대해


```math
\begin{aligned} P_{(X,Y)}(A\times B) &= P_X(A)P_Y(B)\\ &= \left(\int_A p_X(x)\,d\mu(x)\right) \left(\int_B p_Y(y)\,d\nu(y)\right). \end{aligned}
```


Tonelli를 사용하면


```math
= \int_{A\times B} p_X(x)p_Y(y) \,d(\mu\otimes\nu)(x,y).
```


즉 `\(P_{(X,Y)}\)`와 `\(C\mapsto\int_C p_Xp_Y\,d(\mu\otimes\nu)\)`라는 두 확률측도가 모든 rectangle에서 같다. 5절과 같은 π-λ 논증으로 곱 `\(\sigma\)`-대수 전체에서도 같다.

따라서 공동분포의 밀도는


```math
\boxed{ p_{X,Y}(x,y) = p_X(x)p_Y(y) }
```


가 된다.

반대로 공동밀도가


```math
p_{X,Y}(x,y)=p_X(x)p_Y(y)
```


로 factorize된다면


```math
P_{(X,Y)}(A\times B) = P_X(A)P_Y(B)
```


이므로 `\(X,Y\)`는 독립이다.

따라서 밀도가 존재하는 상황에서는


```math
\boxed{ X\perp Y \iff p_{X,Y}(x,y)=p_X(x)p_Y(y) \quad\text{a.e.} }
```


라고 말할 수 있다.

---

# 18. 이번 강의의 내용이 ML에서 쓰이는 곳

이번 강에서 얻은 가장 중요한 구조는


```math
\boxed{ \text{joint distribution} \overset{\text{independence}}{=} \text{product measure} }
```


다.

이 한 줄에서 ML에서 반복해서 등장하는 표현들이 나온다.

### iid dataset


```math
X_1,\dots,X_n\overset{\mathrm{iid}}{\sim}P
```


는


```math
P_{(X_1,\dots,X_n)}=P^{\otimes n}.
```


### 독립 sampling


```math
E[f(X,Y)] = \int f\,d(P_X\otimes P_Y).
```


### nested expectation

Tonelli/Fubini 조건 아래


```math
E[f(X,Y)] = E_X[E_Y[f(X,Y)]].
```


### expectation factorization


```math
E[XY]=E[X]E[Y].
```


### variance reduction of sample mean


```math
\operatorname{Var} \left( \frac1n\sum_{i=1}^nX_i \right) = \frac{\operatorname{Var}(X)}{n}.
```


### density factorization

밀도가 존재한다면


```math
p(x_1,\dots,x_n) = \prod_{i=1}^n p(x_i).
```


즉 머신러닝에서 “iid assumption”이라고 짧게 부르는 가정은 단순한 편의적 표현이 아니다.

데이터셋 전체의 확률측도가


```math
P^{\otimes n}
```


이라는 매우 강한 구조적 가정이다.

---

# 19. 마무리

이번 강에서는 여러 확률변수를 동시에 다루기 위한 무대를 만들었다.

두 측도공간을 합치면


```math
(\mathcal X\times\mathcal Y, \mathcal A\otimes\mathcal B, \mu\otimes\nu)
```


라는 곱측도공간이 생긴다.

곱측도는 measurable rectangle에서


```math
\boxed{ (\mu\otimes\nu)(A\times B) = \mu(A)\nu(B) }
```


로 정의되는 측도다.

그리고 두 확률변수의 공동분포는


```math
\boxed{ P_{(X,Y)} = P\circ(X,Y)^{-1} }
```


라는 곱공간 위의 push-forward 측도였다.

독립성은 이 공동분포가 특별한 형태를 갖는다는 뜻이다.


```math
\boxed{ X\perp Y \iff P_{(X,Y)} = P_X\otimes P_Y. }
```


그 위의 적분을 계산할 때는 Tonelli와 Fubini가 등장했다.


```math
\boxed{ f\ge0 \quad\Longrightarrow\quad \text{Tonelli} } \qquad \boxed{ \int|f|<\infty \quad\Longrightarrow\quad \text{Fubini} }
```


실전에서는


```math
\boxed{ |f|\text{에 Tonelli} \to \text{유한함 확인} \to f\text{에 Fubini} }
```


라고 기억하면 된다.

이제 머신러닝에서 가장 흔한 표기


```math
X_1,\dots,X_n\overset{\mathrm{iid}}{\sim}P
```


의 정확한 의미도 얻었다.


```math
\boxed{ P_{(X_1,\dots,X_n)} = P^{\otimes n}. }
```


그리고 독립이면


```math
E[XY]=E[X]E[Y]
```


가 되며, 밀도가 존재하는 경우에는


```math
p_{X,Y}(x,y) = p_X(x)p_Y(y)
```


까지 내려온다.

그런데 마지막 식에는 이번 강에서 그냥 지나간 단어 하나가 있다.

**밀도.**

우리는 지금까지 너무 자연스럽게


```math
p_X(x)
```


를 써 왔다.

하지만 모든 확률분포에 pdf가 있는 것은 아니다.또 이산분포에는 pmf가 있고 연속분포에는 pdf가 있다고 배웠지만, 둘을 하나의 언어로 표현할 방법은 없을까?

더 근본적으로


```math
\boxed{ \text{"측도 }P\text{가 측도 }\mu\text{에 대한 밀도를 가진다"} }
```


는 것은 정확히 무슨 뜻일까?

그 답이 다음 강의의 출발점이다.


```math
\boxed{ \frac{dP}{d\mu} }
```


이 기호가 무엇을 의미하는지 이해하면 pdf와 pmf가 하나로 합쳐지고, likelihood, KL divergence, importance sampling도 같은 언어로 읽히기 시작한다.

다음 강에서는 **Radon–Nikodym 정리와 밀도**를 다룬다.

---

## 참고

- Rosenthal, _A First Look at Rigorous Probability Theory_
    
- Axler, _Measure, Integration & Real Analysis_
    
- Tao, _An Introduction to Measure Theory_
