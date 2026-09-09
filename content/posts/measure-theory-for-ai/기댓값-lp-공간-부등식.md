---
title: "5강. 기댓값, Lᵖ 공간, 부등식"
date: 2026-09-04
lastmod: 2026-09-09
draft: false
math: true
description: "ERM이 전제하는 손실의 기댓값은 정말 항상 존재하는가에서 출발해, 기댓값이 새로운 연산이 아니라 확률측도에 대한 르베그 적분일 뿐임을 보이고 LOTUS를 push-forward의 적분 공식으로 회수한다. Lᵖ를 '함수 하나가 곧 벡터 하나'인 함수공간으로 소개한 뒤 확률공간에서의 포함관계를 Hölder로 증명하고, Jensen·Hölder·Cauchy–Schwarz·Markov·Chebyshev를 각각 언제 꺼내는 도구인지로 정리한다."
summary: "ERM이 전제하는 손실의 기댓값은 정말 항상 존재하는가에서 출발해, 기댓값이 새로운 연산이 아니라 확률측도에 대한 르베그 적분일 뿐임을 보이고 LOTUS를 push-forward의 적분 공식으로 회수한다. Lᵖ를 '함수 하나가 곧 벡터 하나'인 함수공간으로 소개한 뒤 확률공간에서의 포함관계를 Hölder로 증명하고, Jensen·Hölder·Cauchy–Schwarz·Markov·Chebyshev를 각각 언제 꺼내는 도구인지로 정리한다."
series: "Measure Theory for AI"
series_order: 5
aliases:
  - "/posts/기댓값-lp-공간-부등식/"
vault_source: "Distillation/Study/Measure Theory for AI/원고/5강. 기댓값, Lᵖ 공간, 부등식.md"
---

> **한 줄 요약**: 기댓값은 새로운 연산이 아니라 확률측도에 대한 르베그 적분이다. 그 적분이 존재하는 범위가 `\(L^p\)` 공간이고, 값을 통제하는 도구가 부등식이다.

# 들어가는 말: 평균은 항상 존재하는가?

머신러닝의 목적함수는 거의 언제나 기댓값이다.


```math
\min_\theta\ E_{X\sim P}[\ell(\theta;X)]
```


그리고 우리는 이것을 데이터로 근사한다.


```math
\frac1n\sum_{i=1}^n \ell(\theta;X_i)\ \approx\ E[\ell(\theta;X)]
```


이는 전부


```math
E[\ell(\theta;X)]
```


가 **존재한다**는 전제 위에 서 있다.

그런데 그 전제는 공짜가 아니다.

분포가 멀쩡히 있어도 평균이 아예 존재하지 않을 수 있고, 평균이 있어도 분산이 없을 수 있다.

그래서 이번 강은 세 개의 질문에 순서대로 답한다.


```math
\boxed{ \begin{array}{l} \text{1. }E[X]\text{란 정확히 무엇인가}\\[3pt] \text{2. 어떤 확률변수에 대해 그것이 존재하는가}\\[3pt] \text{3. 존재한다면 얼마나 강하게 통제되는가} \end{array} }
```


1번의 답은 **르베그 적분**이고, 2번의 답은 `\(L^p\)` **공간**이며, 3번의 답은 **부등식**이다.

제목의 세 단어가 그대로 이 세 질문이다.

---

# 요약

이번 강의 흐름은 다음과 같다.

### 1. 기댓값은 새로운 연산이 아니다

확률공간 `\((\Omega,\mathcal F,P)\)` 위의 확률변수 `\(X\)`에 대해


```math
\boxed{ E[X]=\int_\Omega X\,dP }
```


이다.

이산확률변수의 합과 연속확률변수의 적분은 이 하나의 정의에서 나오는 표현이다.

---

### 2. LOTUS는 push-forward의 적분 공식이다

3강에서


```math
P_X=P\circ X^{-1}
```


로 `\(X\)`의 분포를 정의했다.

따라서 적절한 `\(g\)`에 대해


```math
\boxed{ E[g(X)] = \int_\Omega g(X(\omega))\,dP(\omega) = \int_{\mathbb R}g(x)\,dP_X(x) }
```


이다.

이것이 LOTUS(Law of the Unconscious Statistician)다.

새 정리가 갑자기 등장한 것이 아니라 **push-forward의 적분 공식**이다.


---

### 3. 부등식은 각각 역할이 다르다

|도구|핵심 형태|언제 쓰는가|
|---|---|---|
|Jensen|`\(\phi(E[X])\le E[\phi(X)]\)`|비선형 함수와 기댓값의 순서를 비교|
|Hölder|`\(E[\lvert XY\rvert]\le\lVert X\rVert_p\lVert Y\rVert_q\)`|곱의 적분을 각 인자의 `\(L^p\)` 크기로 제어|
|Cauchy–Schwarz|`\(E[\lvert XY\rvert]\le\sqrt{E[X^2]}\sqrt{E[Y^2]}\)`|`\(L^2\)`의 내적·공분산을 제어|
|Markov|`\(P(X\ge a)\le E[X]/a\)`|평균으로 꼬리확률 제어|
|Chebyshev|`\(P(\lvert X-\mu\rvert\ge a)\le\sigma^2/a^2\)`|분산으로 평균에서 벗어날 확률 제어|

---

### 4. 확률공간에서는 큰 `\(p\)`가 더 강한 조건이다

`\(1\le p<q\le\infty\)`이면


```math
\boxed{ L^q(P)\subseteq L^p(P) }
```


이고


```math
\boxed{ \|X\|_p\le\|X\|_q. }
```


위 두 식은 확률공간에서 `\(P(\Omega)=1\)`이기 때문에 가능한 현상이다.

---

# 1. 기댓값 = 르베그 적분

4강에서는 측도공간 `\((\Omega,\mathcal F,\mu)\)` 위에서


```math
\int f\,d\mu
```


라는 기호를 어떻게 만드는지 배웠다.

확률론에서는 특별한 측도 `\(P\)`를 사용한다.

`\(P(\Omega)=1\)`인 측도다.

따라서 확률변수


```math
X:(\Omega,\mathcal F)\to(\mathbb R,\mathcal B(\mathbb R))
```


에 대해 기댓값은 그냥


```math
\boxed{ E[X]:=\int_\Omega X(\omega)\,dP(\omega) }
```


로 정의한다.

기댓값이라는 별도의 적분법이 있는 것이 아니다.


```math
\boxed{ \text{expectation} = \text{Lebesgue integral with respect to }P }
```


이다.

따라서 4강의 모든 적분 정리를 그대로 확률변수에 사용할 수 있다.

예를 들어 `\(X_n\uparrow X\)`이고 `\(X_n\ge0\)`이면 MCT에 의해


```math
E[X_n]\uparrow E[X].
```


`\(X_n\to X\)` a.s.이고


```math
|X_n|\le Y,\qquad E[|Y|]<\infty
```


이면 DCT에 의해


```math
E[X_n]\to E[X].
```


4강에서 적분


```math
\int
```


을 기댓값


```math
E
```


로 바꾸었을 뿐이다.


- a.s. 는 almost surely로 그 사건이 발생할 확률이 1이라는 것
---

## 기댓값이 유한하다는 것은 공짜가 아니다

일반적인 실수값 확률변수 `\(X\)`에 대해


```math
X=X^+-X^-
```


였으므로


```math
E[X] = E[X^+]-E[X^-]
```


이다.

그런데


```math
E[X^+]=E[X^-]=\infty
```


이면


```math
\infty-\infty
```


가 되어 기댓값은 정의되지 않는다.

따라서 특별히 중요한 조건이


```math
\boxed{ E[|X|]<\infty }
```


이다.

이를 `\(X\)`가 **적분가능하다(integrable)**고 한다.

즉


```math
X\in L^1
```


이라는 뜻이다.

이 경우에는


```math
E[X^+]<\infty,\qquad E[X^-]<\infty
```


이므로 `\(E[X]\)`는 확실히 유한하다.


---

## 반례: Cauchy 분포에는 평균이 없다

표준 Cauchy 분포의 밀도는


```math
p(x)=\frac{1}{\pi(1+x^2)}
```


이다.

`\(x=0\)`에 대칭이므로 얼핏


```math
E[X]=0
```


처럼 보인다.

하지만 양의 부분만 적분해 보면


```math
\int_0^\infty x\frac{1}{\pi(1+x^2)}\,dx = \infty.
```


음의 부분도 절댓값 기준으로 똑같이 발산한다.

즉


```math
E[X^+]=E[X^-]=\infty.
```


따라서


```math
\boxed{ E[X]\text{는 존재하지 않는다.} }
```



```math
\boxed{ \text{분포가 있다고 해서 평균까지 자동으로 존재하는 것은 아니다.} }
```


---

# 2. 이산과 연속의 공식은 어디서 나오는가


이산확률변수라면


```math
E[X] = \sum_x xP(X=x),
```


연속확률변수라면


```math
E[X] = \int_{\mathbb R}xp_X(x)\,dx.
```


마치 기댓값에 두 개의 정의가 있는 것처럼 보인다.

하지만 둘 다


```math
E[X]=\int_\Omega X\,dP
```


에서 나온다.

이를 가장 깔끔하게 보여주는 것이 LOTUS다.

---

# 3. LOTUS — 3강 push-forward의 첫 payoff

3강에서 확률변수 `\(X\)`의 분포를


```math
\boxed{ P_X=P\circ X^{-1} }
```


로 정의했다.

즉


```math
P_X(A) = P(X^{-1}(A)) = P(X\in A).
```


원래 확률은 `\(\Omega\)` 위에 있었다.


```math
(\Omega,\mathcal F,P)
```


그런데 `\(X\)`가 이 확률을 실수축으로 밀어내어


```math
(\mathbb R,\mathcal B(\mathbb R),P_X)
```


를 만들었다.

따라서 **Borel 가측** `\(g:\mathbb R\to\mathbb R\)`에 대해


```math
\boxed{ \int_\Omega g(X(\omega))\,dP(\omega) = \int_{\mathbb R}g(x)\,dP_X(x) }
```


이다.

`\(g\ge0\)`이거나 `\(g(X)\)`가 적분가능하면 이 등식이 성립한다. 등식의 증명은 여기서는 생략하겠다.

확률론 표기로 쓰면


```math
\boxed{ E[g(X)] = \int_{\mathbb R}g(x)\,dP_X(x) }
```


이다.

이것이 LOTUS다.

Law of the Unconscious Statistician이라는 이름 때문에 별도의 확률론적 트릭처럼 보이지만, 측도론적으로는 이미 3강에서 본 push-forward의 적분 공식이다.

간단한 예로 확인해보자. `\(X\sim\operatorname{Bernoulli}(p)\)`이면


```math
P_X=(1-p)\delta_0+p\,\delta_1
```


이므로 `\(g(x)=x^2\)`에 LOTUS를 적용하면


```math
E[X^2]=0^2(1-p)+1^2p=p
```


이다. 한편 `\(X\)`는 `\(0\)`과 `\(1\)`만 갖는 지시함수여서 `\(X^2=X\)`이고, 따라서 `\(E[X^2]=E[X]=p\)`다. 두 경로가 같은 값을 준다.


---

## 이산분포가 나오면

`\(X\)`가 `\(x_1,x_2,\dots\)`의 값만 갖는다면


```math
P_X = \sum_i P(X=x_i)\delta_{x_i}
```


이다.

특히 `\(g(x)=x\)`이면


```math
E[X] = \sum_i x_iP(X=x_i)
```


이다.

이제 저 공식이 어떻게 나왔는지 더 살펴보자.

**X가 유한개 값 `\(x_1,\dots,x_n\)`만 갖는다면**


```math
g(X) = \sum_{i=1}^n g(x_i)\mathbf 1_{\{X=x_i\}}
```


이므로 `\(g(X)\)` 자체가 simple function이다. 그러면 4강의 2단계 정의


```math
\int \phi\,d\mu=\sum_k a_k\mu(A_k)
```


가 그대로 답을 준다.


```math
E[g(X)] = \sum_{i=1}^n g(x_i)P(X=x_i)
```


위 식은 유도한 것이 아니라 정의 그대로다.

**X가 가산 무한개의 값을 가질 수 있으면 MCT가 한 번 필요하다.** (MCT는 4강 참조)
`\(S=\{x_1,x_2,\dots\}\)`, `\(S_n=\{x_1,\dots,x_n\}\)`이라 하자. **`\(g\ge0\)`이면**


```math
g\,\mathbf 1_{S_n} \uparrow g\,\mathbf 1_S
```


이므로


```math
E[g(X)] = \lim_{n\to\infty}\sum_{i=1}^n g(x_i)P(X=x_i) = \sum_{i=1}^\infty g(x_i)P(X=x_i).
```


여기에는 극한이 있다. 하지만 정의역을 잘게 쪼개는 극한이 아니라 급수의 부분합 극한이다.

**두 등호는 하는 일이 다르다.** 첫 번째 등호에는 세 단계가 묶여 있다.


```math
\int_{\mathbb R} g\,dP_X
\;\overset{(1)}{=}\; \int_S g\,dP_X
\;\overset{(2)}{=}\; \lim_n \int g\,\mathbf 1_{S_n}\,dP_X
\;\overset{(3)}{=}\; \lim_n\sum_{i=1}^n g(x_i)P(X=x_i)
```


|단계|근거|
|---|---|
|(1)|`\(P_X(S^c)=0\)`이므로 측도 `\(0\)`인 곳은 적분에 보이지 않는다|
|(2)|MCT|
|(3)|각 `\(n\)`에서 앞의 유한 단계|

두 번째 등호는 급수 기호의 정의다. `\(\sum_{i=1}^\infty a_i:=\lim_n\sum_{i=1}^n a_i\)`이다.

다만 정의일 뿐이라고 넘기기 전에 확인할 것이 하나 있다. 좌변 `\(\int g\,dP_X\)`에는 나열 순서가 없는데 우변 `\(\sum_{i=1}^\infty\)`는 나열 `\(x_1,x_2,\dots\)`에 의존한다. 이 등호는 나열을 바꿔도 값이 같다는 것을 함께 주장하고 있다. `\(g\ge0\)`이면 비음급수를 유한 부분집합에 대한 합의 상한으로 쓸 수 있어서 순서가 개입하지 않는다.

**일반 `\(g\)`는 `\(g^+\)`와 `\(g^-\)`로 쪼갠다.** `\(g\)`가 음수값을 가지면 `\(g\,\mathbf 1_{S_n}\)`이 단조증가가 아니어서 위의 MCT를 그대로 쓸 수 없다. 대신 `\(g^\pm\ge0\)`에 각각 적용한 뒤 빼면 되고, `\(g(X)\)`가 적분가능하면 급수가 절대수렴하므로 나열 순서에 무관하다.


---

## 밀도가 존재하면

`\(P_X\)`가 Lebesgue 측도에 대해 밀도 `\(p_X\)`를 갖는다면


```math
dP_X(x)=p_X(x)\,dx
```


이므로


```math
E[g(X)] = \int_{\mathbb R}g(x)p_X(x)\,dx.
```


특히 `\(g(x)=x\)`이면


```math
E[X] = \int_{\mathbb R}xp_X(x)\,dx.
```


단 `\(dP_X(x)=p_X(x)\,dx\)`는 **유도한 것이 아니라 가정이다.**  밀도가 존재할 조건(`\(P_X\)`가 Lebesgue 측도에 대해 절대연속)과, 그 조건에서 밀도를 실제로 만들어내는 일은 8강 Radon–Nikodym 정리에서 설명하겠다.

그리고 이 가정은 항상 성립하는 건 아니다. 3강의 Cantor 분포는 이산도 아니고 Lebesgue 밀도도 없다. 그런 분포에서도


```math
\int g\,dP_X
```


는 아무 문제 없이 정의된다. 두 공식은 계산이 편해지는 두 경우일 뿐이고, 적분 자체는 그보다 큰 범위에서 할 수 있다.

즉 우리가 알고 있던 두 공식은


```math
\boxed{ E[g(X)] = \int g\,dP_X }
```


라는 하나의 식이 각각 counting measure와 Lebesgue measure의 언어로 표현된 것이다.


---

# 4. `\(L^p\)` 공간 — 얼마나 적분가능한가

## 왜 "공간"이라고 부르는가

정의를 쓰기 전에 이름부터 짚고 가자.

익숙한 벡터공간은 보통 `\(\mathbb R^n\)`이다. 벡터는 숫자 `\(n\)`개를 나열한 것이고, 길이와 내적은 좌표로 계산한다.

확률변수도 똑같이 볼 수 있다.

표본공간이 유한해서


```math
\Omega=\{\omega_1,\dots,\omega_n\}
```


이라고 하자. 확률변수 `\(X:\Omega\to\mathbb R\)`는 각 `\(\omega_i\)`에 숫자 하나를 배정하는 것이므로


```math
\boxed{ X \ \longleftrightarrow\ (X(\omega_1),\dots,X(\omega_n))\in\mathbb R^n }
```


이다. 확률변수가 곧 배정표이고, 배정표가 곧 벡터다.

`\(\Omega\)`가 무한하면 성분의 개수가 무한해질 뿐 발상은 같다. 이렇게 **함수 하나를 점 하나로 보는 공간**을 함수공간(function space)이라 한다.

낯선 개념이 아니다. 이미 쓰고 있다.

- 신호 `\(f(t)\)`를 기저함수들의 합으로 분해하는 Fourier 급수는 함수공간에서의 직교분해다

- 최소제곱 `\(\min_x\|b-Ax\|\)`는 `\(b\)`를 `\(A\)`의 열공간 위로 사영하는 것이다


다음 강에서 하는 일이 정확히 이 두 가지를 **확률변수들의 공간에서** 반복하는 것이다.

다만 무한차원에서는 `\(\mathbb R^n\)`에 없던 문제가 하나 생긴다.

성분이 무한히 많아지면 **길이(노름)가 발산할 수 있다.**

그래서 "모든 함수"를 원소로 받을 수는 없고, 어디까지 받을지 기준을 정해야 한다.

그 기준이 적분가능성이고, 기준을 재는 눈금이 `\(p\)`다.

---

## 정의


기댓값이 존재하는지를 묻는 조건은


```math
E[|X|]<\infty
```


였다.

이번에는 조금 더 일반적으로


```math
E[|X|^p]<\infty
```


인 확률변수들을 모아보자.

`\(1\le p<\infty\)`에 대해


```math
\boxed{ L^p(\Omega,\mathcal F,P) = \left\{ X:\ E[|X|^p]<\infty \right\} }
```


라고 쓴다.

그리고


```math
\boxed{ \|X\|_p = \left(E[|X|^p]\right)^{1/p} }
```


를 `\(L^p\)` norm이라 부른다.

특히


```math
L^1: \quad E|X|<\infty
```


는 기댓값을 안정적으로 다룰 수 있는 공간이고,


```math
L^2: \quad E[X^2]<\infty
```


는 분산과 평균제곱오차를 다룰 수 있는 공간이다.

마지막으로 `\(p=\infty\)`는 지수 자리에 `\(\infty\)`를 대입할 수 없으니 따로 정의한다. 적분 대신 **거의 확실한 상한**을 쓴다.


```math
\boxed{ \|X\|_\infty := \operatorname{ess\,sup}|X| = \inf\{M\ge0:\ |X|\le M\ \text{a.s.}\} }
```


그리고


```math
L^\infty = \{X:\ \|X\|_\infty<\infty\}
```


는 유계인 확률변수들의 공간이다.

그냥 `\(\sup\)`가 아니라 essential supremum인 이유는 바로 다음 절과 같다. 확률 `\(0\)`인 집합 위에서 `\(|X|\)`가 아무리 커도 무시한다. `\(\Omega=[0,1]\)` 위의 균등분포에서 `\(X\)`가 유리수 점에서만 `\(10^{100}\)`이고 나머지에서 `\(0\)`이라면 `\(\sup|X|=10^{100}\)`이지만 `\(\|X\|_\infty=0\)`이다.

이름이 어긋나지 않는다는 것도 확인해 둘 만하다. `\(p\to\infty\)`이면


```math
\|X\|_p\longrightarrow\|X\|_\infty
```


이므로 `\(\infty\)`라는 첨자는 극한의 자리를 그대로 물려받은 것이다.

---

## 그런데 이것은 그대로는 norm이 아니다

4강에서 측도 `\(0\)`인 집합은 적분에서 보이지 않는다고 했다.

만약


```math
X=Y\qquad\text{a.s.}
```


이면


```math
E[|X-Y|^p]=0
```


이므로


```math
\|X-Y\|_p=0.
```


하지만 함수로서 `\(X\)`와 `\(Y\)`가 모든 점에서 같은 것은 아닐 수도 있다.

따라서 확률변수를 점별 함수 그대로 보면 `\(\|\cdot\|_p\)`는 엄밀히 말해 seminorm이다.

이를 해결하는 방법은 간단하다.


```math
\boxed{ X=Y\text{ a.s.이면 같은 원소로 취급한다.} }
```


즉 `\(L^p\)`는 실제로는 거의 확실하게 같은 함수들을 하나로 묶은 **동치류의 공간**이다.

이렇게 하면


```math
\|X\|_p=0 \quad\Longrightarrow\quad X=0\text{ in }L^p
```


가 되어 진짜 norm이 된다.

4강에서 배운


```math
\boxed{ \text{측도 0인 집합은 적분에서 보이지 않는다} }
```


가 이제 공간 자체의 정의에 들어온 것이다.

---

# 5. 확률공간에서 `\(L^p\)`의 포함관계

`\(p\)`가 커질수록


```math
E[|X|^p]<\infty
```


라는 조건은 더 강해진다.

확률공간에서는


```math
1\le p<q\le\infty
```


이면 


```math
\boxed{ L^q\subseteq L^p. }
```


뿐만 아니라


```math
\boxed{ \|X\|_p\le\|X\|_q. }
```


예를 들어


```math
L^4\subset L^2\subset L^1.
```


4차 moment가 유한하면 2차 moment도 유한하고, 2차 moment가 유한하면 1차 moment도 유한하다.

- 확률변수 `\(X\)`의 **`\(k\)`차 moment**란


```math
E[X^k]
```


를 말하고, 절대값을 씌운


```math
E[|X|^k]
```


를 **`\(k\)`차 absolute moment**라 한다. `\(L^p\)`에서 유한성을 따질 때는 항상 후자이므로


```math
\boxed{ k\text{차 moment가 유한하다} \iff E[|X|^k]<\infty \iff X\in L^k }
```


가 된다. 즉 바로 위의 `\(L^4\subset L^2\subset L^1\)`을 moment의 언어로 옮긴 것이 이 문장이다.


- 일반적인 무한측도에서는 `\(L^q\)` 와 `\(L^p\)`가 **서로 포함관계가 없다**

- 위 두 부등식의 증명은 §7 끝의 「§5 포함관계의 증명」에서 다룬다

---

# 6. Jensen — 비선형 함수와 평균의 순서

이제 확률론에서 계속 등장하는 부등식을 네 묶음으로 정리하자.

첫 번째는 Jensen 부등식이다.

`\(\phi:\mathbb R\to\mathbb R\)`가 convex이고 필요한 적분들이 존재하면


```math
\boxed{ \phi(E[X]) \le E[\phi(X)]. }
```


convex 함수에서는


```math
\text{평균을 먼저 넣는 것}
```


보다


```math
\text{함수를 적용한 뒤 평균내는 것}
```


이 더 크다.

그림으로 보면 convex 함수의 chord가 graph 위에 놓이는 성질의 확률 버전이다.

반대로 `\(\phi\)`가 concave이면 부등호가 뒤집힌다.


```math
\boxed{ E[\phi(X)] \le \phi(E[X]). }
```


---

## ML에서 Jensen

`\(\log x\)`는 concave이므로


```math
\boxed{ E[\log X]\le\log E[X]. }
```


variational inference에서 ELBO를 만들 때 등장하는 Jensen 부등식도 바로 이것이다.

복잡한 비선형 함수가 기댓값 바깥과 안 중 어느 쪽에 있을 때 더 큰지를 결정해야 한다면 Jensen을 먼저 떠올리면 된다.


```math
\boxed{ \text{nonlinearity와 expectation의 순서를 비교한다} \;\longrightarrow\; \text{Jensen} }
```


---

# 7. Hölder와 Cauchy–Schwarz — 곱을 제어한다

## Hölder 부등식

두 번째 도구는 Hölder 부등식이다.

`\(1<p,q<\infty\)`가


```math
\frac1p+\frac1q=1
```


을 만족한다고 하자.

이때


```math
X\in L^p,\qquad Y\in L^q
```


이면


```math
XY\in L^1
```


이고


```math
\boxed{ E[|XY|] \le \|X\|_p\|Y\|_q. }
```


즉 두 함수를 곱했을 때 그 적분이 얼마나 커질 수 있는지를 각 함수의 `\(L^p\)` 크기로 제어한다.

### 등호 조건

Hölder는 Young 부등식


```math
ab\le\frac{a^p}{p}+\frac{b^q}{q}\qquad(a,b\ge0)
```


을 적분해서 얻는데(`\(a=\frac{|X|}{\|X\|_{p}},b=\frac{|Y|}{\|Y\|_q}\)`), Young의 등호는 `\(a^p=b^q\)`일 때만 성립한다. 그래서 Hölder의 등호도 이 조건이 거의 확실하게(`\(\text{a.s.}\)`) 성립할 때다.


```math
\boxed{ E[|XY|]=\|X\|_p\|Y\|_q \iff \alpha|X|^p=\beta|Y|^q \ \text{a.s.} }
```


여기서 `\(\alpha,\beta\ge0\)`는 동시에 `\(0\)`은 아닌 상수다. `\(X,Y\)`가 모두 `\(0\)`이 아니면 `\(q=\frac{p}{p-1}\)`이므로


```math
|Y|=c\,|X|^{p-1}\quad\text{a.s.}\qquad(c>0)
```


로 쓸 수 있다. 비례하는 것이 `\(|X|\)`와 `\(|Y|\)`가 아니라 `\(|X|^p\)`와 `\(|Y|^q\)`라는 점에 주의한다.


```math
\boxed{ \text{product를 제어한다} \;\longrightarrow\; \text{Hölder} }
```


---

## Cauchy–Schwarz 부등식


특히


```math
p=q=2
```


이면


```math
\boxed{ E[|XY|] \le \sqrt{E[X^2]}\sqrt{E[Y^2]}. }
```


이것이 Cauchy–Schwarz 부등식이다.

여기에 적분의 삼각부등식 `\(|E[XY]|\le E[|XY|]\)`를 앞에 붙이면


```math
|E[XY]| \;\le\; E[|XY|] \;\le\; \|X\|_2\|Y\|_2
```


가 된다. 6강에서 정의할 내적 `\(\langle X,Y\rangle=E[XY]\)`로 쓰면


```math
\boxed{ |\langle X,Y\rangle| \le \|X\|_2\|Y\|_2. }
```


유클리드 공간의


```math
|x^\top y| \le \|x\|\|y\|
```


와 완전히 같은 식이다.

이것은 우연이 아니다.

`\(L^2\)` 자체가 내적공간이기 때문이다.

### 등호 조건


```math
\boxed{ |E[XY]|=\|X\|_2\|Y\|_2 \iff \alpha X=\beta Y \ \text{a.s.} }
```


역시 `\((\alpha,\beta)\neq(0,0)\)`인 상수이고, 요컨대 `\(X\)`와 `\(Y\)`가 **선형종속**일 때다. `\(Y\neq0\)`이면 `\(X=tY\)` a.s.인 `\(t\)`가 존재한다는 말과 같다.

이 조건은 Hölder 등호 조건에 `\(p=q=2\)`를 넣어서는 나오지 않는다. C–S가 사실 두 단계 부등식이기 때문이다.


```math
|E[XY]| \;\le\; E[|XY|] \;\le\; \|X\|_2\|Y\|_2
```


두 번째 등호는 `\(|X|\propto|Y|\)` a.s.이면 충분하지만, 첫 번째 등호는 `\(XY\)`가 **부호를 바꾸지 않을 것**을 추가로 요구한다. 두 조건이 합쳐져야 선형종속이 된다. 아래 절에서 이 간극을 반례로 확인한다.

---

## 두 등호 조건은 왜 다른가

Hölder에서 `\(p=q=2\)`로 특수화하는 것만으로는 등호 조건이 나오지 않는다. Hölder의 등호 조건은 `\(|X|^p\propto|Y|^q\)`인데, 여기에 `\(p=q=2\)`를 넣으면


```math
|X|\propto|Y| \quad\text{a.s.}
```


까지밖에 얻지 못한다. 이것은 선형종속보다 약하다.

`\(\Omega\)`를 확률 `\(\tfrac12\)`씩 `\(A,A^c\)`로 나누고 `\(A\)` 위에서 `\(Y=X\)`, `\(A^c\)` 위에서 `\(Y=-X\)`로 두어 보자. `\(|X|=|Y|\)`이므로


```math
E[|XY|]=E[X^2]=\|X\|_2\|Y\|_2
```


로 Hölder 등호가 성립한다. 한편 `\(XY\)`는 `\(A\)`에서 `\(X^2\)`, `\(A^c\)`에서 `\(-X^2\)`이므로


```math
E[XY]=E[X^2;A]-E[X^2;A^c]
```


이다. `\(X^2\)`의 질량이 양쪽에 절반씩 실리도록 — 예컨대 `\(|X|\)`를 상수로 — 잡으면 `\(E[XY]=0\)`이어서


```math
|\langle X,Y\rangle|=0<\|X\|_2\|Y\|_2
```


이고, `\(X\)`와 `\(Y\)`는 선형종속도 아니다. `\(A\)`에서는 `\(t=1\)`, `\(A^c\)`에서는 `\(t=-1\)`이 필요한데 `\(\Omega\)` 전체를 덮는 하나의 `\(t\)`는 없기 때문이다.

C–S의 증명은 등호 조건을 함께 준다. 모든 `\(t\in\mathbb R\)`에 대해


```math
0\le E[(X-tY)^2] = E[X^2]-2tE[XY]+t^2E[Y^2]
```


이다. 우변은 `\(t\)`에 대한 이차식이면서 음이 되지 않으므로 판별식이 `\(0\)` 이하다.


```math
(E[XY])^2 \le E[X^2]\,E[Y^2]
```


이것이 C–S다. 판별식이 `\(0\)`이 되는 것은 어떤 `\(t\)`에서 `\(E[(X-tY)^2]=0\)`일 때, 즉


```math
\boxed{ \text{등호} \iff X=tY\ \text{a.s.인 }t\text{가 존재한다} }
```


일 때다. 이 조건이 6강에서 `\(|\rho_{X,Y}|=1\)`의 의미를 결정한다.

---

## §5 포함관계의 증명

§5에서 결과만 제시한 `\(\|X\|_p\le\|X\|_q\)`와 `\(L^q\subseteq L^p\)`를 이제 Hölder로 증명한다. 핵심은 `\(|X|^p\)`를 **상수함수 `\(1\)`과의 곱**으로 보는 것이다. `\(1\le p<q<\infty\)`에 대해


```math
E[|X|^p]=E\big[|X|^p\cdot 1\big]
```


Hölder 진술을 자리 이름으로 다시 쓰면


```math
E[|UV|]\le\|U\|_r\,\|V\|_{r'},\qquad \frac1r+\frac1{r'}=1
```


이다. 네 자리에 넣는 것은 다음과 같다.


```math
U=|X|^p,\qquad V=1,\qquad r=\frac{q}{p}>1,\qquad r'=\frac{q}{q-p}
```


`\(U\)` 자리에 들어가는 것이 `\(X\)`가 아니라 `\(|X|^p\)`라는 점에 주의한다. 또한 「Hölder 부등식」 절의 `\(p,q\)`는 켤레지수였지만 여기서 `\(p,q\)`는 `\(L^p,L^q\)`의 두 지수이므로, 켤레지수 자리는 `\(r,r'\)`으로 따로 둔다. 실제로 `\(\frac1r+\frac1{r'}=\frac pq+\frac{q-p}q=1\)`이다.

두 노름을 계산하면 지수가 맞아떨어진다.


```math
\|U\|_r=\Big(E\big[(|X|^p)^{q/p}\big]\Big)^{p/q}=\big(E[|X|^q]\big)^{p/q}
```



```math
\|V\|_{r'}=\big(E[1^{r'}]\big)^{1/r'}=\big(E[1]\big)^{(q-p)/q}
```


따라서 Hölder를 적용하면


```math
E\big[|X|^p\cdot 1\big]\;\le\;\big(E[|X|^{q}]\big)^{p/q}\,\big(E[1]\big)^{(q-p)/q}
```


이고 `\(E[1]=P(\Omega)=1\)`이므로 뒤 인자가 통째로 사라진다.


```math
E[|X|^p]\le\big(E[|X|^q]\big)^{p/q}
```


양변을 `\(\frac1p\)`제곱하면


```math
\boxed{ \|X\|_p\le\|X\|_q \quad\Longrightarrow\quad L^q\subseteq L^p }
```


**`\(q=\infty\)`인 경우**는 Hölder까지 갈 필요가 없다. 정의상 `\(|X|\le\|X\|_\infty\)`가 a.s. 성립하므로


```math
E[|X|^p]\;\le\;\|X\|_\infty^p\,E[1]\;=\;\|X\|_\infty^p
```


이고, 양변을 `\(\frac1p\)`제곱하면 `\(\|X\|_p\le\|X\|_\infty\)`다. 여기서도 결정적인 것은 `\(E[1]=P(\Omega)=1\)`이라는 사실이다.

일반적인 무한측도 공간이라면 `\(\|1\|_{r'}=\mu(\Omega)^{1/r'}=\infty\)`가 되어 이 논법이 무너지고, 실제로 포함관계도 성립하지 않는다.

---

# 8. Markov와 Chebyshev — moment에서 tail로

지금까지의 부등식이 적분 자체를 제어했다면, Markov와 Chebyshev는 기댓값 정보를 **확률 bound**로 바꾼다.

먼저 `\(X\ge0\)`이고 `\(a>0\)`라고 하자.

사건 `\(\{X\ge a\}\)` 위에서는


```math
X\ge a
```


이므로


```math
X \ge a\mathbf 1_{\{X\ge a\}}.
```


양변의 기댓값을 취하면


```math
E[X] \ge aE[\mathbf 1_{\{X\ge a\}}].
```


그런데


```math
E[\mathbf 1_A]=P(A)
```


였으므로


```math
E[X] \ge aP(X\ge a).
```


따라서


```math
\boxed{ P(X\ge a) \le \frac{E[X]}{a}. }
```


이것이 Markov 부등식이다.

---

## Chebyshev는 Markov를 제곱에 적용한 것이다

평균


```math
\mu=E[X]
```


과 분산


```math
\sigma^2=\operatorname{Var}(X)
```


가 유한하다고 하자.

음이 아닌 확률변수


```math
(X-\mu)^2
```


에 Markov를 적용하면


```math
\begin{aligned} P(|X-\mu|\ge a) &= P((X-\mu)^2\ge a^2)\\ &\le \frac{E[(X-\mu)^2]}{a^2}. \end{aligned}
```


따라서


```math
\boxed{ P(|X-\mu|\ge a) \le \frac{\sigma^2}{a^2}. }
```


이것이 Chebyshev 부등식이다.

즉 둘은 별개의 공식이라기보다


```math
\boxed{ \text{Markov} \quad \xrightarrow{\,X\mapsto(X-E[X])^2\,} \quad \text{Chebyshev} }
```


관계다.

---

## 부등식을 언제 꺼낼 것인가

공식을 외우는 것보다 질문을 기억하는 편이 낫다.

- 비선형 함수와 기댓값의 순서를 비교해야 하는가  
    `\(\longrightarrow\)` **Jensen**
    
- `\(XY\)` 같은 곱의 적분을 제어해야 하는가  
    `\(\longrightarrow\)` **Hölder**
    
- `\(L^2\)`에서 내적이나 covariance를 제어하는가  
    `\(\longrightarrow\)` **Cauchy–Schwarz**
    
- 음이 아닌 확률변수의 평균만 알고 tail probability를 묻는가  
    `\(\longrightarrow\)` **Markov**
    
- 평균과 분산을 알고 평균에서 멀리 벗어날 확률을 묻는가  
    `\(\longrightarrow\)` **Chebyshev**
    


```math
\boxed{ \begin{array}{c} \text{nonlinearity}\to\text{Jensen}\\ \text{product}\to\text{Hölder}\\ \text{inner product}\to\text{Cauchy--Schwarz}\\ \text{mean}\to\text{tail}\to\text{Markov}\\ \text{variance}\to\text{tail}\to\text{Chebyshev} \end{array} }
```



---

# 9. 이 강의의 내용이 앞으로 쓰이는 곳

이번 강의 산출물은 두 개다.

## A. 기댓값 = 적분


```math
\boxed{ E[X]=\int X\,dP }
```


이제부터 확률론의 모든 평균 계산은 르베그 적분의 계산이다.

7강에서는 여러 확률변수를 함께 적분하면서 Fubini와 Tonelli를 사용하고,

9강에서는


```math
E[Y\mid\mathcal G]
```


를 다시 적분의 등식으로 정의한다.

---

## B. `\(L^p\)` = 적분가능성의 등급


```math
\boxed{ L^1,\quad L^2,\quad L^p }
```


는 단지 함수들의 집합이 아니라 “어느 moment까지 통제할 수 있는가”를 나타내는 공간이다.

확률공간에서는


```math
q>p \quad\Longrightarrow\quad L^q\subset L^p.
```


앞으로

- `\(L^1\)`: 기댓값과 조건부 기댓값
    
- `\(L^2\)`: 분산, 회귀, martingale
    
- 더 높은 moment: concentration과 수렴성
    

에서 계속 등장한다.

---

# 10. 마무리

4강에서는 가측함수를 적분하는 방법을 만들었다.


```math
\boxed{ \mathbf 1_A \longrightarrow \text{simple} \longrightarrow f\ge0 \longrightarrow f^+-f^- }
```


이번 강에서는 그 적분에 확률측도 `\(P\)`를 넣었을 뿐인데


```math
\boxed{ E[X]=\int X\,dP }
```


가 되었고, push-forward를 이용해


```math
\boxed{ E[g(X)] = \int g\,dP_X }
```


라는 LOTUS를 얻었다.

그다음 "적분이 되는가"를 정도의 문제로 바꾸어


```math
L^1\supset L^2\supset L^4\supset\cdots
```


라는 등급을 만들었고, 그 등급 위에서 값을 통제하는 다섯 개의 부등식을 정리했다.


```math
\boxed{ \begin{array}{c} \text{nonlinearity}\to\text{Jensen}\\ \text{product}\to\text{Hölder}\\ \text{inner product}\to\text{Cauchy--Schwarz}\\ \text{mean}\to\text{tail}\to\text{Markov}\\ \text{variance}\to\text{tail}\to\text{Chebyshev} \end{array} }
```


여기까지가 "기댓값을 안전하게 다루는 법"이다.

그런데 `\(L^p\)` 중 하나가 눈에 띈다.


```math
L^2
```


다.

Cauchy–Schwarz를 다시 보자.


```math
E[|XY|]\le\sqrt{E[X^2]}\sqrt{E[Y^2]}
```


이 부등식은 `\(E[XY]\)`라는 양이 `\(X\)`와 `\(Y\)`의 크기로 제어된다고 말한다. 그런데 유클리드 공간에서 정확히 같은 모양의 부등식을 본 적이 있다.


```math
|\langle x,y\rangle|\le\|x\|\,\|y\|
```


우연이 아니다.


```math
\boxed{ E[XY]\ \text{는 내적이다.} }
```


이것을 인정하는 순간 평균·분산·공분산·상관계수가 전부 길이와 각도로 바뀌고, 최소제곱은 직교사영이 된다.

그것이 다음 강의 내용이다.


```math
\boxed{ \text{적분가능성의 등급} \quad\longrightarrow\quad L^2\text{의 기하학} }
```


다음: [6강. L² 기하와 사영 정리](/posts/measure-theory-for-ai/l2-기하와-사영-정리/)

---

## 참고

- Rosenthal, _A First Look at Rigorous Probability Theory_
    
- Axler, _Measure, Integration & Real Analysis_
    
- Tao, _An Introduction to Measure Theory_
