---
title: "8강. Radon–Nikodym과 밀도 — pdf, likelihood, KL"
date: 2026-09-11
lastmod: 2026-09-21
draft: false
math: true
description: "모든 확률분포에 정말 pdf가 있는가. 밀도는 기준측도에 대한 비율 dP/dμ이고, 이 비율이 존재할 조건인 절대연속을 이해하면 pdf·pmf·likelihood·KL·importance weight가 한 언어로 읽힌다."
summary: "Dirac 측도에 Lebesgue 밀도가 없다는 관찰에서 출발해, 밀도가 존재할 조건인 절대연속 P≪μ와 두 측도가 서로 다른 곳에 사는 특이 P⊥μ를 정의한다. Lebesgue 분해정리로 분포를 밀도 부분과 특이 부분으로 나누고, Radon–Nikodym 정리가 절대연속 부분을 함수 dP/dμ 하나로 바꿔 줌을 확인한다. pdf와 pmf가 기준측도만 다른 같은 RN derivative임을 보인 뒤 likelihood, likelihood ratio, KL divergence, importance weight를 모두 dP/dQ로 읽고, P≪Q가 깨질 때 KL이 무한대가 되는 이유를 manifold 위의 GAN으로 확인한다. 조건부 기댓값의 존재가 RN 정리의 귀결임을 보이며 다음 강을 준비한다."
series: "Measure Theory for AI"
series_order: 8
aliases:
  - "/posts/radon-nikodym과-밀도/"
vault_source: "Distillation/Study/Measure Theory for AI/원고/8강. Radon-Nikodym과 밀도.md"
---

> **한 줄 요약**: 밀도 `\(dP/d\mu\)`란 “`\(\mu\)`로 잰 부피에 비해 `\(P\)`가 얼마나 질량을 놓는가”를 나타내는 함수다. 단, `\(\mu\)`가 `\(0\)`이라고 보는 곳에 `\(P\)`가 질량을 놓으면 이 비율은 존재할 수 없다. 이 하나의 원리에서 pdf, pmf, likelihood, KL divergence, importance sampling이 모두 나온다.

## 들어가는 말: 모든 확률분포에는 정말 pdf가 있을까?

확률론을 처음 배울 때 우리는 확률분포를 대체로 두 종류로 나눈다.

연속확률변수에는 pdf가 있고


```math
P(X\in A)=\int_A p(x)\,dx
```


라고 쓴다.

이산확률변수에는 pmf가 있고


```math
P(X\in A)=\sum_{x\in A}p(x)
```


라고 쓴다.

그래서 자연스럽게 이런 인상을 받는다.


```math
\boxed{\text{확률분포에는 어떤 식으로든 }p(x)\text{가 있다.}}
```


하지만 3강에서 이미 이 생각을 깨뜨리는 분포를 하나 만났다.

**Cantor 분포**다.

Cantor 분포는 한 점에 양의 확률을 주지 않으므로 pmf가 없다. 동시에 Lebesgue 측도에 대해 밀도를 갖지도 않으므로 pdf도 없다.

더 단순한 예도 있다.


```math
P=\delta_0
```


를 생각해 보자. 모든 질량이 `\(0\)` 한 점에 모여 있는 Dirac measure다.

만약 Lebesgue 측도 `\(\lambda\)`에 대한 어떤 pdf `\(p\)`가 존재해서


```math
\delta_0(A)=\int_A p(x)\,d\lambda(x)
```


라고 쓸 수 있다고 하자.

그런데


```math
\lambda(\{0\})=0
```


이므로 어떤 적분가능한 `\(p\)`에 대해서도


```math
\int_{\{0\}}p\,d\lambda=0
```


이다.

반면


```math
\delta_0(\{0\})=1.
```


모순이다.

즉


```math
\boxed{\delta_0\text{는 Lebesgue 측도에 대한 밀도를 갖지 않는다.}}
```


여기서 문제의 핵심이 보인다.

pdf가 존재하려면 `\(P\)`가 마음대로 질량을 놓을 수 있는 것이 아니다. 기준이 되는 측도 `\(\mu\)`가

> “여기는 부피가 `\(0\)`이다.”

라고 선언한 곳에는 `\(P\)` 역시 질량을 놓지 않아야 한다.

이 조건이 **절대연속**(absolute continuity)이고, 그 조건 아래 밀도의 존재를 보장하는 정리가 **Radon–Nikodym 정리**다.

이번 강에서는


```math
\boxed{ \text{absolute continuity} \to \text{Radon–Nikodym derivative} \to \text{density} }
```


라는 구조를 만든 뒤


```math
\boxed{ \text{pdf},\quad \text{pmf},\quad \text{likelihood},\quad \text{KL},\quad \text{importance weight} }
```


가 사실 모두 같은 물건의 다른 모습임을 확인한다.

---

# 요약

이번 강의 흐름은 다음과 같다.

### 1. 밀도는 혼자 존재하지 않는다

밀도는 항상


```math
\frac{dP}{d\mu}
```


처럼 **어떤 기준측도 `\(\mu\)`에 대한 밀도**다.

같은 확률분포 `\(P\)`라도 기준측도를 바꾸면 밀도의 모양이 달라진다.

---

### 2. 밀도가 존재하려면 `\(P\ll\mu\)`여야 한다


```math
\boxed{ P\ll\mu \iff \mu(A)=0\Rightarrow P(A)=0 }
```


이다.

즉 `\(\mu\)`가 보지 못하는 곳에 `\(P\)`가 질량을 놓지 않아야 한다.

---

### 3. 모든 측도는 밀도 부분과 특이 부분으로 나뉜다

적절한 조건 아래


```math
\boxed{ P=P_{\mathrm{ac}}+P_{\mathrm{s}}, \qquad P_{\mathrm{ac}}\ll\mu, \qquad P_{\mathrm{s}}\perp\mu. }
```


이것이 Lebesgue 분해정리다.

---

### 4. 절대연속인 부분은 함수 하나로 표현된다

Radon–Nikodym 정리에 의해


```math
P\ll\mu
```


이면 어떤 가측함수 `\(p\ge0\)`가 존재해서


```math
\boxed{ P(A)=\int_A p\,d\mu }
```


가 된다.

이 함수가


```math
\boxed{ p=\frac{dP}{d\mu} }
```


다.

---

### 5. KL과 importance sampling은 같은 RN derivative를 사용한다


```math
\boxed{ D_{\mathrm{KL}}(P\|Q) = E_P\left[ \log\frac{dP}{dQ} \right] }
```


이고


```math
\boxed{ E_P[f] = E_Q\left[ f\frac{dP}{dQ} \right]. }
```


둘 다 핵심은


```math
\frac{dP}{dQ}
```


라는 **확률측도 사이의 상대적인 밀도**다.

---

# 1. 밀도는 기준 측도가 필요하다

우리는 흔히


```math
p(x)
```


를 그냥 “분포의 밀도”라고 부른다.

하지만 측도론적으로는 이 표현이 불완전하다.

정확한 질문은


```math
\boxed{ \text{무엇에 대한 밀도인가?} }
```


다.

예를 들어 표준정규분포 `\(P=N(0,1)\)`의 익숙한 pdf는


```math
p(x)=\frac1{\sqrt{2\pi}}e^{-x^2/2}
```


다.

정확히 쓰면 이것은


```math
\boxed{ p=\frac{dP}{d\lambda} }
```


이다.

여기서 `\(\lambda\)`는 `\(\mathbb R\)` 위의 Lebesgue 측도다.

즉


```math
P(A) = \int_A \frac{dP}{d\lambda}(x)\,d\lambda(x).
```


우리가 평소 쓰는


```math
P(X\in A)=\int_Ap(x)\,dx
```


에서 `\(dx\)`는 사실


```math
d\lambda(x)
```


를 줄여 쓴 것이다.

따라서 pdf란 특별한 새로운 개념이 아니다.


```math
\boxed{ \text{pdf} = \text{Lebesgue measure에 대한 RN derivative} }
```


다.

이 관점을 얻는 순간 “연속분포에는 pdf가 있다”라는 문장이 정확하지 않다는 것도 보인다.

정확한 문장은


```math
\boxed{ P\ll\lambda \text{인 분포에는 Lebesgue density가 있다.} }
```


다.

---

# 2. 절대연속 — 기준측도가 못 보는 곳에 질량을 놓지 않는다

두 측도 `\(P,\mu\)`가 같은 가측공간 `\((\mathcal X,\mathcal A)\)` 위에 있다고 하자.

`\(P\)`가 `\(\mu\)`에 대해 **절대연속**(absolutely continuous)이라는 것은


```math
\boxed{ \mu(A)=0 \quad\Longrightarrow\quad P(A)=0 }
```


가 모든 `\(A\in\mathcal A\)`에 대해 성립한다는 뜻이다.

기호로


```math
\boxed{ P\ll\mu }
```


라고 쓴다.

직관은 간단하다.


```math
\boxed{ \mu\text{가 무시하는 집합을 }P\text{도 무시한다.} }
```


다.

---

## Gaussian은 Lebesgue 측도에 대해 절대연속이다


```math
P=N(0,1)
```


이라 하자.

어떤 집합 `\(A\)`가


```math
\lambda(A)=0
```


이면


```math
P(A) = \int_A \frac1{\sqrt{2\pi}}e^{-x^2/2}\,dx =0.
```


따라서


```math
N(0,1)\ll\lambda.
```


이것이 Gaussian pdf가 존재할 수 있는 근본적인 이유다.

---

## Dirac measure는 Lebesgue 측도에 대해 절대연속이 아니다

반면


```math
P=\delta_0
```


라면


```math
\lambda(\{0\})=0
```


이지만


```math
\delta_0(\{0\})=1.
```


따라서


```math
\boxed{ \delta_0\not\ll\lambda. }
```


Radon–Nikodym 정리가 적용될 조건 자체가 깨진다.

그래서 Lebesgue pdf가 존재하지 않는다.

---

# 3. 특이성 — 두 측도가 서로 다른 곳에 산다

절대연속과 함께 자주 등장하는 개념이 **특이**(mutually singular)다.

두 측도 `\(P,Q\)`가 특이라는 것은 어떤 가측집합 `\(S\)`가 있어서


```math
P(S^c)=0, \qquad Q(S)=0
```


가 된다는 뜻이다.

기호로


```math
\boxed{ P\perp Q }
```


라고 쓴다.

즉 `\(P\)`의 질량은 모두 `\(S\)` 안에 있고, `\(Q\)`는 그 `\(S\)`에 전혀 질량을 두지 않는다.

측도론적으로


```math
\boxed{ P\text{와 }Q\text{가 서로 다른 곳에 산다.} }
```


고 생각할 수 있다.

---

## 예: Dirac과 Gaussian


```math
P=\delta_0, \qquad Q=N(0,1)
```


라 하자.

`\(S=\{0\}\)`로 잡으면


```math
P(S)=1, \qquad Q(S)=0.
```


따라서


```math
\boxed{ \delta_0\perp N(0,1). }
```


---

## 예: `\([0,1]\)` 위의 연속 균등분포와 두 점 균등분포


```math
P=\operatorname{Unif}[0,1]
```


이고


```math
Q=\frac12\delta_0+\frac12\delta_1
```


이라 하자.

`\(Q\)`는 두 점 `\(\{0,1\}\)`에만 살고, `\(P\)`는 그 두 점에 질량을 두지 않는다. 정의의 모양에 맞추려면


```math
S=\mathbb R\setminus\{0,1\}
```


로 잡으면 된다.


```math
P(S^c)=P(\{0,1\})=0, \qquad Q(S)=0.
```


따라서


```math
P\perp Q.
```


---

## 반대로 비퇴화 Gaussian끼리는 서로 절대연속이다

`\(X\sim N(\mu,\Sigma)\)`의 covariance `\(\Sigma\)`가 positive definite, 즉


```math
\operatorname{Var}(v^\top X)=v^\top\Sigma v>0 \qquad (\forall\, v\neq 0)
```


이면 이 Gaussian을 **비퇴화**(non-degenerate)라고 한다.

어느 방향으로 봐도 분산이 0이 아니라는 뜻이다.

`\(\mathbb R^d\)`에서 covariance가 positive definite인 두 Gaussian


```math
P=N(\mu_1,\Sigma_1), \qquad Q=N(\mu_2,\Sigma_2)
```


를 생각하자.

두 분포의 Lebesgue density는 모든 `\(x\in\mathbb R^d\)`에서 양수다.

따라서


```math
P\ll Q, \qquad Q\ll P.
```


이 경우


```math
\boxed{ P\sim Q }
```


라고 쓰고 두 측도가 **equivalent**하다고 한다.

평균이 아주 멀리 떨어져 있어도 마찬가지다.

확률질량이 대부분 다른 곳에 있다는 것과, 질량이 사는 집합 자체가 완전히 갈라지는 것(특이)은 다른 이야기다.

---

# 4. manifold 위의 분포는 왜 `\(\mathbb R^d\)` pdf가 없을까

이번에는 `\(\mathbb R^2\)` 안의 원


```math
S^1=\{(x,y):x^2+y^2=1\}
```


위에서만 데이터가 나온다고 하자.

예를 들어 원 위의 arc length에 대해 균일한 확률분포 `\(P\)`를 생각할 수 있다.

이 분포는


```math
P(S^1)=1
```


이다.

하지만 2차원 Lebesgue 측도에서는


```math
\lambda^2(S^1)=0.
```


따라서


```math
P\not\ll\lambda^2.
```


오히려


```math
\boxed{ P\perp\lambda^2. }
```


다.

그래서 이 분포는 `\(\mathbb R^2\)`의 Lebesgue 측도에 대한 pdf를 가질 수 없다.

이것이

> “저차원 manifold 위에 놓인 데이터 분포는 ambient Lebesgue density를 갖지 않는다.”

라는 말의 정확한 의미다.

그렇다고 밀도라는 개념 자체가 사라지는 것은 아니다.

원 자체의 길이측도 `\(\mu_{S^1}\)`를 기준측도로 쓰면


```math
P\ll\mu_{S^1}
```


이고


```math
\frac{dP}{d\mu_{S^1}}
```


를 정의할 수 있다.

즉


```math
\boxed{ \text{ambient space에 대한 density는 없어도 manifold의 부피측도에 대한 density는 있을 수 있다.} }
```


이 관점은 이 시리즈의 후속편(확률 미분기하)에서 다시 돌아온다.

---

# 5. 절대연속과 특이는 서로의 단순한 반대말이 아니다

여기서 주의할 점이 하나 있다.


```math
P\not\ll\mu
```


라고 해서 반드시


```math
P\perp\mu
```


인 것은 아니다.

예를 들어


```math
P = 0.7\,N(0,1) + 0.3\,\delta_0
```


를 생각하자.

이 분포의 `\(70\%\)`는 Gaussian처럼 Lebesgue 측도 위에 퍼져 있고, `\(30\%\)`는 `\(0\)` 한 점에 붙어 있다.

`\(P\)`는 Lebesgue 측도에 대해 절대연속이 아니다.

왜냐하면


```math
\lambda(\{0\})=0
```


이지만


```math
P(\{0\})=0.3
```


이기 때문이다.

그렇다고 `\(P\perp\lambda\)`도 아니다. Gaussian 부분은 Lebesgue 측도와 같은 공간에 퍼져 있다.

즉 이 분포에는

- Lebesgue density로 표현할 수 있는 부분
- Lebesgue density로 표현할 수 없는 singular 부분

이 동시에 들어 있다.

이 둘을 정확하게 분리해 주는 정리가 Lebesgue 분해정리다.

---

# 6. Lebesgue 분해정리 — 모든 측도를 density 부분과 singular 부분으로 나눈다

`\(P\)`가 확률측도이고 `\(\mu\)`가 `\(\sigma\)`-유한 측도라고 하자.

그러면 `\(P\)`는 유일하게


```math
\boxed{ P=P_{\mathrm{ac}}+P_{\mathrm{s}} }
```


로 분해된다.

여기서


```math
P_{\mathrm{ac}}\ll\mu
```


이고


```math
P_{\mathrm{s}}\perp\mu.
```


즉


```math
\boxed{ \text{모든 }\sigma\text{-유한 측도} = \text{기준측도에 대해 density를 가질 수 있는 부분} + \text{기준측도와 특이한 부분}. }
```


앞의 예에서는


```math
P_{\mathrm{ac}} = 0.7\,N(0,1), \qquad P_{\mathrm{s}} = 0.3\,\delta_0
```


이다.

Lebesgue 측도 `\(\lambda\)`를 기준으로 보면


```math
0.7N(0,1)
```


부분은 pdf로 표현되고


```math
0.3\delta_0
```


부분은 표현되지 않는다.

---

# 7. Radon–Nikodym 정리 — 언제 측도를 함수 하나로 바꿀 수 있는가

이제 이번 강의의 핵심 정리다.

같은 가측공간 위에 두 `\(\sigma\)`-유한 측도 `\(P,\mu\)`가 있고


```math
P\ll\mu
```


라고 하자.

그러면 어떤 가측함수


```math
f:\mathcal X\to[0,\infty]
```


가 존재해서 모든 `\(A\in\mathcal A\)`에 대해


```math
\boxed{ P(A)=\int_A f\,d\mu }
```


가 된다.

그리고 이 `\(f\)`는 `\(\mu\)`-거의 모든 곳(a.e.)에서 유일하다.

이를


```math
\boxed{ f=\frac{dP}{d\mu} }
```


라고 쓴다.

이것이 **Radon–Nikodym theorem**이다.

---

## `\(dP/d\mu\)`는 숫자끼리 나누는 것이 아니다

표기를 보면


```math
\frac{dP}{d\mu}
```


가 마치


```math
\frac{P(dx)}{\mu(dx)}
```


같은 점별 나눗셈처럼 보인다.

하지만 이것이 정의는 아니다.

RN derivative의 정의는 오직


```math
\boxed{ P(A) = \int_A \frac{dP}{d\mu}\,d\mu \qquad \forall A }
```


라는 적분 관계다.

다만 `\(\mathbb R^d\)`에서 충분히 좋은 경우에는 Lebesgue differentiation theorem에 의해 작은 공 `\(B_r(x)\)`를 사용한 비율


```math
\frac{P(B_r(x))}{\mu(B_r(x))}
```


의 극한으로 밀도를 회수할 수 있다.

그래서

> “`\(\mu\)`로 잰 단위 부피당 `\(P\)`의 질량”

이라는 직관은 좋다.

하지만 수학적 정의는 적분 등식이다.

---

# 8. pdf와 pmf는 사실 같은 개념이다

이제 학부 확률론의 두 공식을 하나로 합칠 수 있다.

---

## pdf

`\(\mathbb R^d\)` 위의 확률측도 `\(P\)`가 Lebesgue 측도 `\(\lambda^d\)`에 대해 절대연속이면


```math
\boxed{ p(x)=\frac{dP}{d\lambda^d}(x) }
```


를 pdf라고 한다.

따라서


```math
P(A) = \int_Ap(x)\,dx.
```


---

## pmf

이번에는 countable state space


```math
\mathcal X=\{x_1,x_2,\dots\}
```


를 생각하자.

그 위의 counting measure `\(\#\)`를


```math
\#(A)=A\text{에 들어 있는 점의 개수}
```


로 정의한다.

그러면


```math
\int_A f\,d\# = \sum_{x\in A}f(x).
```


따라서 확률측도 `\(P\)`에 대해


```math
p(x)=P(\{x\})
```


라 놓으면


```math
P(A) = \sum_{x\in A}p(x) = \int_Ap\,d\#.
```


즉


```math
\boxed{ p=\frac{dP}{d\#}. }
```


따라서


```math
\boxed{ \text{pdf} = \frac{dP}{d(\text{Lebesgue})}, \qquad \text{pmf} = \frac{dP}{d(\text{counting})}. }
```


둘은 다른 개념이 아니었다.

**기준측도가 달랐을 뿐이다.**

---

# 9. density는 분포 자체가 아니라 분포와 기준측도의 관계다

이 관점에서 중요한 사실 하나가 나온다.

같은 `\(P\)`라도 기준측도 `\(\mu\)`를 바꾸면


```math
\frac{dP}{d\mu}
```


도 바뀐다.

심지어 앞에서 본 혼합분포


```math
P = 0.7N(0,1)+0.3\delta_0
```


도 적절한 기준측도를 고르면 하나의 density로 표현할 수 있다.

예를 들어


```math
\mu=\lambda+\delta_0
```


라고 하자.

그러면 `\(P\ll\mu\)`다.

따라서 RN derivative가 존재한다.

표준정규 pdf를 `\(\phi\)`라 하면 한 version을


```math
\frac{dP}{d\mu}(x) = \begin{cases} 0.7\phi(x), & x\neq0,\\ 0.3, & x=0 \end{cases}
```


처럼 잡을 수 있다.

Lebesgue 부분과 atom을 하나의 함수 안에 넣은 것이다.

따라서


```math
\boxed{ \text{“이 분포는 density가 있는가?”} }
```


라는 질문은 사실 불완전하다.

정확한 질문은


```math
\boxed{ \text{“이 분포는 어떤 기준측도 }\mu\text{에 대해 density가 있는가?”} }
```


다.

극단적으로는 모든 확률측도 `\(P\)`에 대해


```math
P\ll P
```


이므로


```math
\boxed{ \frac{dP}{dP}=1 \quad P\text{-a.e.} }
```


다.

density는 분포가 혼자 가지고 있는 속성이 아니다.

---

# 10. RN derivative의 chain rule

RN derivative는 미분처럼 보이는 표기만 가진 것이 아니라 실제로 미분과 비슷한 계산법을 가진다.

측도


```math
P\ll Q\ll R
```


가 있다고 하자.

그러면


```math
\boxed{ \frac{dP}{dR} = \frac{dP}{dQ} \frac{dQ}{dR} \qquad R\text{-a.e.} }
```


가 성립한다.

이것이 RN derivative의 chain rule이다.

특히 `\(P,Q\)`가 모두 공통 기준측도 `\(\mu\)`에 대해 density를 가지고


```math
p=\frac{dP}{d\mu}, \qquad q=\frac{dQ}{d\mu}
```


라고 하자.

그리고 `\(P\ll Q\)`라면


```math
\boxed{ \frac{dP}{dQ} = \frac{p}{q} \qquad Q\text{-a.e.} }
```


가 된다.

우리가 ML에서 끊임없이 보는


```math
\frac{p(x)}{q(x)}
```


라는 비율의 근본적인 형태가 이것이다.

density ratio는 사실


```math
\boxed{ \frac{dP}{dQ} }
```


다.

---

# 11. 측도 변환 공식 — expectation의 기준분포를 바꾼다

RN derivative의 가장 중요한 계산법은 이것이다.


```math
P\ll Q
```


라고 하자.

그러면 음이 아닌 가측함수 또는 적절히 적분가능한 `\(f\)`에 대해


```math
\boxed{ \int f\,dP = \int f\frac{dP}{dQ}\,dQ. }
```


확률론 표기로 쓰면


```math
\boxed{ E_{X\sim P}[f(X)] = E_{X\sim Q} \left[ f(X)\frac{dP}{dQ}(X) \right]. }
```


이것을 **change of measure**라고 볼 수 있다.

`\(P\)`에서 계산하고 싶었던 적분을 `\(Q\)`에서 계산하되


```math
\frac{dP}{dQ}
```


라는 보정값을 곱해 주는 것이다.

이 식은 뒤의 importance sampling 설명에서 사용된다.

---

# 12. likelihood는 무엇의 밀도인가

이제 통계학의 likelihood를 보자.

파라미터 `\(\theta\)`에 따라 확률분포가 달라지는 statistical model


```math
\{P_\theta:\theta\in\Theta\}
```


가 있다고 하자.

그리고 모든 `\(P_\theta\)`가 하나의 공통 기준측도 `\(\mu\)`에 대해 절대연속이라고 하자.


```math
P_\theta\ll\mu.
```


그러면 RN 정리에 의해


```math
p_\theta(x) = \frac{dP_\theta}{d\mu}(x)
```


를 정의할 수 있다.

관측값 `\(x\)`를 고정하고 이것을 `\(\theta\)`의 함수로 바라본 것이 likelihood다.


```math
\boxed{ L(\theta;x) = \frac{dP_\theta}{d\mu}(x). }
```


Lebesgue 밀도가 있는(`\(P_\theta\ll\lambda\)`) 분포라면 `\(\mu=\lambda\)`를 사용하여 익숙한 pdf가 되고, 가산집합 위의 이산분포라면 counting measure를 사용하여 pmf가 된다.

따라서 MLE의


```math
\hat\theta_{\mathrm{MLE}} = \arg\max_\theta p_\theta(x)
```


라는 식은 더 정확히 말하면


```math
\boxed{ \hat\theta_{\mathrm{MLE}} = \arg\max_\theta \frac{dP_\theta}{d\mu}(x). }
```


다.

---

## likelihood는 `\(P(X=x)\)`가 아니다

연속분포에서


```math
P_\theta(X=x)=0
```


이다.

그런데도 likelihood


```math
p_\theta(x)
```


는 양수일 수 있다.

따라서 likelihood를

> “관측값 `\(x\)`가 나올 확률”

이라고 부르는 것은 엄밀하지 않다.

정확히는


```math
\boxed{ \text{기준측도의 단위 부피에 비해 }P_\theta \text{가 }x\text{ 주변에 얼마나 많은 질량을 두는가} }
```


를 나타내는 density다.

여기에 미묘한 점이 하나 더 있다. 7절에서 RN derivative는 `\(\mu\)`-a.e.로만 유일하다고 했다. 그런데 `\(\mu=\lambda\)`이면 한 점 `\(\{x\}\)`는 영집합이다. 따라서 관측된 한 점에서의 값 `\(p_\theta(x)\)`는 원리적으로 version을 어떻게 고르느냐에 따라 얼마든지 달라질 수 있다.

그래도 likelihood를 문제없이 계산할 수 있는 것은 Gaussian처럼 **연속인 version**이 있으면 그것을 쓰기로 약속하기 때문이다. 두 연속함수가 `\(\lambda\)`-a.e.로 같으면 모든 점에서 같으므로, 이 약속이 한 점에서의 값을 하나로 고정한다.

---

## 기준측도를 바꾸면 likelihood 값 자체는 바뀔 수 있다

density가 기준측도에 의존하므로 likelihood의 수치 역시 기준측도에 의존한다.

하지만 `\(\theta\)`에 의존하지 않는 다른 공통 기준측도로 바꾸면 모든 likelihood에 `\(x\)`에만 의존하는 같은 factor가 곱해진다.

따라서 일반적인 조건에서


```math
\arg\max_\theta L(\theta;x)
```


는 변하지 않는다.

MLE가 density의 절대적인 숫자보다 **파라미터 사이의 상대적인 비교**를 사용하기 때문이다.

---

# 13. likelihood ratio는 측도 사이의 RN derivative다

두 파라미터 `\(\theta_0,\theta_1\)`을 비교한다고 하자.


```math
P_{\theta_1}\ll P_{\theta_0}.
```


그러면


```math
\boxed{ \frac{dP_{\theta_1}}{dP_{\theta_0}}(x) }
```


를 정의할 수 있다.

공통 기준측도 `\(\mu\)`에 대한 density가 있다면


```math
\frac{dP_{\theta_1}}{dP_{\theta_0}}(x) = \frac{p_{\theta_1}(x)}{p_{\theta_0}(x)}
```


이다.

즉 익숙한 **likelihood ratio**


```math
\boxed{ \frac{p_{\theta_1}(x)}{p_{\theta_0}(x)} }
```


는 사실 확률측도 자체 사이의 RN derivative다.

10절의 density ratio, 그리고 17절에서 볼 importance weight도 마찬가지다.

- likelihood ratio
- density ratio
- importance weight

는 이름만 다를 뿐 모두 `\(\frac{dP}{dQ}\)`다.

---

# 14. KL divergence의 진짜 정의

두 확률측도 `\(P,Q\)`가 있고


```math
P\ll Q
```


라고 하자.

그러면 KL divergence를


```math
\boxed{ D_{\mathrm{KL}}(P\|Q) = \int \log\left( \frac{dP}{dQ} \right)dP }
```


로 정의한다.

즉


```math
\boxed{ D_{\mathrm{KL}}(P\|Q) = E_P \left[ \log\frac{dP}{dQ} \right]. }
```


공통 기준측도 `\(\mu\)`에 대한 density `\(p,q\)`가 있다면


```math
\frac{dP}{dQ} = \frac pq
```


이므로 익숙한


```math
\boxed{ D_{\mathrm{KL}}(P\|Q) = \int p(x) \log\frac{p(x)}{q(x)} \,d\mu(x) }
```


가 나온다.

즉 `\(p\log(p/q)\)`가 근본적인 정의가 아니라 다음이 근본이다.


```math
\boxed{ \log\frac{dP}{dQ}. }
```


---

## KL은 항상 정의된다

정의를 그대로 보면 걸리는 점이 하나 있다.

`\(\frac{dP}{dQ}<1\)`인 곳에서 `\(\log\frac{dP}{dQ}\)`는 음수다. 양수 부분의 적분과 음수 부분의 적분이 둘 다 무한대라면 `\(\infty-\infty\)`가 되어 KL이 정의되지 않을 것이다. 결론만 말하자면 KL은 음이 아닌 함수의 적분으로 항상 정의된다.

자세히 살펴보자. `\(r=\frac{dP}{dQ}\)`라 두고 11절의 측도 변환으로 적분을 `\(Q\)` 위로 옮기면


```math
D_{\mathrm{KL}}(P\|Q) = \int \log r\,dP = \int r\log r\,dQ
```


다. (측도 변환은 `\(\log r\)`의 양수 부분과 음수 부분에 각각 적용하면 된다.)

여기서 값이 `\(0\)`인 적분


```math
\int (r-1)\,dQ = P(\mathcal X)-Q(\mathcal X) = 0
```


을 빼 주면


```math
\boxed{ D_{\mathrm{KL}}(P\|Q) = \int \big(r\log r-r+1\big)\,dQ }
```


가 된다.

피적분함수에 나온 `\(\phi(t)=t\log t-t+1\)`은 `\(t\ge0\)`에서 항상 `\(0\)` 이상이다. 

즉 KL은 **음이 아닌 함수의 적분**이다. 4강에서 본 것처럼 이런 적분은 값이 `\(+\infty\)`가 될 수는 있어도 정의되지 않는 일은 없다. KL은 언제나 `\([0,\infty]\)` 안의 값을 가지고, “`\(D_{\mathrm{KL}}=\infty\)`”는 정의가 안 된다는 말이 아니라 무한대라는 정당한 값이다.

덤으로 하나가 더 따라온다. `\(\phi(t)=0\)`은 `\(t=1\)`일 때뿐이므로, `\(D_{\mathrm{KL}}(P\|Q)=0\)`이면 `\(r=1\)` `\(Q\)`-a.e.이고 따라서 `\(P=Q\)`다.


---

## KL은 density ratio의 평균 log다

이제 `\(\frac{dP}{dQ}\)` 자체는 무엇을 뜻하는지 보자. `\(\mathbb R^d\)`에서라면 점 `\(x\)`에서의 값은 `\(x\)` 근처 작은 공에 두 측도가 놓는 질량의 비로 읽을 수 있다.


```math
\frac{dP}{dQ}(x)=\lim_{r\to0}\frac{P(B_r(x))}{Q(B_r(x))} \qquad (Q\text{-a.e. } x)
```


즉 `\(\frac{dP}{dQ}(x)\)`가 크다는 것은 `\(x\)` 근처에 `\(P\)`가 `\(Q\)`보다 그 배율만큼 더 많은 질량을 놓는다는 뜻이다.

이 질량의 비는 그대로 통계적 의미를 갖는다. `\(P(B_r(x))\)`와 `\(Q(B_r(x))\)`는 각각 “`\(X\sim P\)`”와 “`\(X\sim Q\)`”일 때 `\(X\)`가 `\(x\)` 근처에 떨어질 확률이다. 그래서 `\(X=x\)`라는 관측 하나는 “`\(X\sim Q\)`”보다 “`\(X\sim P\)`” 쪽으로 odds를 `\(\frac{dP}{dQ}(x)\)`배 밀어준다(아래 곁가지). odds는 곱셈으로 갱신되므로 log를 취하면 덧셈이 되고,


```math
\log\frac{dP}{dQ}(x)
```


는 관측 하나가 `\(P\)` 쪽에 보태는 증거량, 곧 **log likelihood ratio**가 된다.

이제 `\(X\)`를 실제로 `\(P\)`에서 뽑아 이 증거량을 평균내면, 그것이 바로 위에서 정의한 KL이다.


```math
\boxed{ \mathrm{KL} = \text{expected log likelihood ratio}. }
```


---

## 곁가지: odds란 무엇인가

위에서 “odds를 `\(\frac{dP}{dQ}(X)\)`배 밀어준다”고 했다. 사건 `\(A\)`의 **odds**(오즈, 승산)는 `\(A\)`가 일어날 확률과 일어나지 않을 확률의 비다.


```math
\mathrm{odds}(A)=\frac{\Pr(A)}{\Pr(A^c)}=\frac{\Pr(A)}{1-\Pr(A)}
```


`\(\Pr(A)=0.75\)`이면 odds는 `\(3\)`이고, 이것이 흔히 말하는 “3 대 1”이다.

`\(P\ll Q\)`라 하고, 두 가설 `\(H_P: X\sim P\)`와 `\(H_Q: X\sim Q\)`에 사전확률 `\(\pi_P,\pi_Q\)`를 준 뒤 `\(X=x\)`를 관측하면


```math
\boxed{ \underbrace{\frac{\Pr(H_P\mid x)}{\Pr(H_Q\mid x)}}_{\text{사후 odds}}
=\underbrace{\frac{\pi_P}{\pi_Q}}_{\text{사전 odds}}\cdot\frac{dP}{dQ}(x) }
```


이다. 두 가설의 사후확률을 나누면 Bayes 정리의 분모가 약분되어 이 식이 된다. 유도는 10강에서 측도론적 베이즈 정리와 함께 다룬다.

양변에 log를 취하면 곱셈이 덧셈이 된다.


```math
\log(\text{사후 odds})=\log(\text{사전 odds})+\log\frac{dP}{dQ}(x)
```


본문에서 말한 증거량이 이 식의 마지막 항이다.

---

# 15. `\(P\not\ll Q\)`이면 KL은 왜 무한대인가

KL 정의에서 절대연속 조건은 장식이 아니다.

만약


```math
P\not\ll Q
```


라면 어떤 집합 `\(A\)`가 있어서


```math
Q(A)=0
```


인데


```math
P(A)>0
```


이다.

즉 `\(P\)`가 질량을 놓는 곳을 `\(Q\)`는 불가능하다고 본다.

density 표기로 생각하면 그곳에서는 직관적으로


```math
\frac{p}{q} = \frac{\text{positive}}{0}
```


가 된다.

그래서 확장된 정의에서는


```math
\boxed{ P\not\ll Q \quad\Longrightarrow\quad D_{\mathrm{KL}}(P\|Q)=+\infty. }
```


라고 둔다.

약속처럼 보이지만 이유가 있다. 14절의 odds로 읽으면 `\(X\)`가 `\(A\)`에 떨어지는 순간 “`\(X\sim Q\)`”는 완전히 배제되고(사후 odds `\(=\infty\)`), 이런 관측이 `\(P\)` 아래에서 확률 `\(P(A)>0\)`로 일어나므로 증거량의 평균인 KL도 무한대일 수밖에 없다.

이것이 KL에서 **support mismatch**가 치명적인 이유다.

---

## 예: Dirac과 Gaussian


```math
P=\delta_0, \qquad Q=N(0,1)
```


라 하자.


```math
Q(\{0\})=0
```


이지만


```math
P(\{0\})=1.
```


따라서


```math
P\not\ll Q
```


이고


```math
\boxed{ D_{\mathrm{KL}}(\delta_0\|N(0,1)) = \infty. }
```


반대 방향도


```math
N(0,1)\not\ll\delta_0
```


이므로 무한대다.

두 측도는 서로 특이하기 때문이다.

---

# 16. manifold와 GAN의 support mismatch

이제 생성모델의 고전적인 문제를 살펴보자.

3강 17절에서 GAN의 생성분포 `\(P_g=G_{\#}P_z\)`에는 Lebesgue 밀도가 없다는 것을 보였고, KL divergence처럼 밀도를 비교하는 척도도 같은 벽에 부딪힌다고 예고했다. 그 이유를 이제 절대연속의 언어로 쓸 수 있다.

실제 데이터 분포 `\(P_{\mathrm{data}}\)`가 `\(\mathbb R^d\)` 안의 저차원 manifold `\(M\)`에 놓여 있다고 하자.

생성모델 분포 `\(P_g\)`도 다른 저차원 manifold `\(N\)` 위에 놓인다고 하자.

만약 두 manifold가 서로 만나지 않거나, 교집합이 각 분포에 대해 measure zero인 정도로만 만난다면 두 분포는 서로 특이하다.


```math
P_{\mathrm{data}}\perp P_g.
```


그러면


```math
P_{\mathrm{data}}\not\ll P_g
```


이고


```math
P_g\not\ll P_{\mathrm{data}}.
```


따라서


```math
D_{\mathrm{KL}}(P_{\mathrm{data}}\|P_g)=\infty
```


이고 반대 방향도 무한대가 된다.

즉 두 support가 실제로 분리된 이상적인 상황에서는


```math
\boxed{ \text{density ratio 자체가 잘 정의되지 않는 영역이 생긴다.} }
```


반대로 두 분포가 같은 manifold 위에 놓여 있고 그 manifold의 부피측도에 대해 각각 density를 가진다면


```math
\frac{dP}{dQ}
```


가 다시 의미를 가질 수 있다.

---

## 곁가지: 교집합이 있어도 왜 특이한가

위에서 두 manifold가 만나더라도 교집합이 measure zero인 정도로만 만난다면 두 분포는 서로 특이하다고 했다. 만나지 않는 경우는 그렇다 쳐도, 실제로 만나는데 “서로 다른 곳에 산다”는 것은 조금 이상하게 들린다. 3절의 정의로 돌아가 `\(S\)`를 직접 찾아보자.

두 분포는 각자 자기 manifold 위에 산다.


```math
P_{\mathrm{data}}(M^c)=0, \qquad P_g(N^c)=0
```


(`\(\mathbb R^d\)` 안의 매끄러운 부분다양체는 Borel 집합이므로 아래에 나오는 집합은 모두 가측이다.)

두 manifold가 만나지 않으면(`\(M\cap N=\varnothing\)`) `\(M\subset N^c\)`이다. 이때는 `\(S=M\)`으로 잡으면 된다.


```math
P_{\mathrm{data}}(S^c)=P_{\mathrm{data}}(M^c)=0, \qquad P_g(S)\le P_g(N^c)=0
```


두 manifold가 만나더라도 교집합이 두 분포 모두에게 질량 0이면, `\(M\)`에서 교집합을 도려낸 `\(S=M\setminus N\)`을 잡는다. `\(S^c=M^c\cup(M\cap N)\)`이므로


```math
P_{\mathrm{data}}(S^c)\le P_{\mathrm{data}}(M^c)+P_{\mathrm{data}}(M\cap N)=0
```


이고, `\(S\)`는 `\(N\)`과 겹치지 않으므로 `\(S\subset N^c\)`, 따라서


```math
P_g(S)\le P_g(N^c)=0
```


이다. 어느 경우든 `\(P_{\mathrm{data}}\perp P_g\)`다.

---

# 17. Importance sampling = RN derivative로 측도를 바꾼다

우리가 원하는 것은


```math
E_{X\sim P}[f(X)]
```


인데 `\(P\)`에서 직접 sampling하기 어렵다고 하자.

대신 sampling하기 쉬운 분포 `\(Q\)`가 있다고 하자.

만약


```math
P\ll Q
```


라면 change-of-measure formula에 의해


```math
\boxed{ E_P[f] = E_Q \left[ f\frac{dP}{dQ} \right]. }
```


따라서


```math
X_1,\dots,X_n\overset{\mathrm{iid}}{\sim}Q
```


를 뽑으면


```math
\boxed{ \hat I_n = \frac1n \sum_{i=1}^n f(X_i) \frac{dP}{dQ}(X_i) }
```


로 `\(E_P[f]\)`를 추정할 수 있다.

이것이 **importance sampling**이다.

---

## density가 있다면 익숙한 `\(p/q\)`가 나온다

`\(P,Q\)`가 공통 기준측도 `\(\mu\)`에 대해


```math
p=\frac{dP}{d\mu}, \qquad q=\frac{dQ}{d\mu}
```


라는 density를 가진다면


```math
\frac{dP}{dQ} = \frac pq.
```


따라서


```math
\boxed{ E_P[f] = E_Q \left[ f(X)\frac{p(X)}{q(X)} \right]. }
```


우리가 importance sampling에서 보던


```math
w(x)=\frac{p(x)}{q(x)}
```


는 사실


```math
\boxed{ w=\frac{dP}{dQ}. }
```


즉 **importance weight는 RN derivative다.**

---

# 18. Importance sampling에서 support 조건이 왜 필요한가

보통 importance sampling을 설명할 때


```math
q(x)>0 \quad\text{whenever}\quad p(x)>0
```


여야 한다고 말한다.

이것은 측도론적으로 정확히


```math
\boxed{ P\ll Q }
```


라는 조건이다.

만약 `\(P\)`가 질량을 두는 어떤 영역에서 `\(Q\)`가 확률 `\(0\)`이라면, `\(Q\)`에서 아무리 많은 샘플을 뽑아도 그 영역을 절대로 방문할 수 없다.

가중치를 아무리 잘 설계해도


```math
\boxed{ \text{볼 수 없는 영역의 질량을 복원할 수는 없다.} }
```


따라서 importance sampling의 support condition은 RN derivative가 존재하기 위한 조건이다.

---

## 절대연속만으로 좋은 importance sampling이 보장되지는 않는다

`\(P\ll Q\)`이면 공식 자체는 성립한다.

하지만 이것이 좋은 Monte Carlo estimator를 보장하는 것은 아니다.

예를 들어 어떤 영역에서


```math
q(x)
```


는 매우 작지만


```math
p(x)
```


는 크다면


```math
\frac{dP}{dQ}(x)
```


가 매우 커질 수 있다.

그러면 소수의 sample이 전체 estimator를 지배한다.

즉


```math
\boxed{ P\ll Q }
```


는 **가능성의 조건**이고,


```math
\boxed{ \frac{dP}{dQ}\text{가 지나치게 변하지 않는가} }
```


는 **통계적 효율의 조건**이다.

importance sampling에서 “proposal `\(Q\)`가 target `\(P\)`와 잘 겹쳐야 한다”는 말이 이것이다.

---

# 19. MPPI에서 등장하는 가중치도 같은 언어다

Model Predictive Path Integral control에서는 한 점 `\(x\)`의 분포가 아니라 전체 trajectory


```math
\tau=(x_0,u_0,x_1,u_1,\dots)
```


의 분포를 생각한다.

즉 표본공간 자체가 **경로공간**(path space)이다.

서로 다른 control law를 사용하면 경로공간 위에 서로 다른 확률측도


```math
P,\qquad Q
```


가 생긴다.

이때 한 경로측도 아래의 expectation을 다른 경로측도 아래에서 계산하려면 다시


```math
\boxed{ \frac{dP}{dQ} }
```


가 필요하다.

확률미분방정식까지 가면 이 경로측도 사이의 RN derivative를 구해 주는 대표적인 결과가 **Girsanov theorem**이고, path integral control이나 MPPI에서 등장하는 exponential weight와 연결된다.

이 시리즈에서는 그 공식까지 유도하지는 않는다.

중요한 것은 구조다.


```math
\boxed{ \text{importance sampling on points} \quad\text{and}\quad \text{importance sampling on trajectories} }
```


는 본질적으로 같은 측도 변환 문제다.

---

# 20. 이번 강의 내용을 ML 언어로 번역하면

이번 강에서 얻은 가장 중요한 구조는


```math
\boxed{ P\ll Q \quad\Longrightarrow\quad \frac{dP}{dQ}\text{가 존재한다.} }
```


다.

이 한 줄에서 여러 ML 표현이 나온다.

### pdf


```math
\boxed{ p(x)=\frac{dP}{d\lambda}(x) }
```


### pmf

countable state space에서


```math
\boxed{ p(x)=\frac{dP}{d\#}(x) }
```


### likelihood

공통 dominating measure `\(\mu\)` 아래에서


```math
\boxed{ L(\theta;x) = \frac{dP_\theta}{d\mu}(x) }
```


### likelihood ratio


```math
\boxed{ \frac{L(\theta_1;x)}{L(\theta_0;x)} = \frac{dP_{\theta_1}}{dP_{\theta_0}}(x) }
```


적절한 절대연속 조건 아래에서다.

### KL divergence


```math
\boxed{ D_{\mathrm{KL}}(P\|Q) = E_P \left[ \log\frac{dP}{dQ} \right] }
```


### importance weight


```math
\boxed{ w(x) = \frac{dP}{dQ}(x) }
```


### change of measure


```math
\boxed{ E_P[f] = E_Q \left[ f\frac{dP}{dQ} \right]. }
```


겉보기에는 서로 전혀 다른 개념들이지만 전부 같은 질문에서 출발한다.


```math
\boxed{ \text{“측도 }P\text{를 측도 }Q\text{의 질량 단위로 표현하면 비율이 얼마인가?”} }
```


그 답이 RN derivative다.

---

# 21. 다음 강의 준비: 조건부 기댓값의 존재가 왜 RN 정리인가

RN 정리가 왜 다음 강의에 필요한지 보자.

확률공간


```math
(\Omega,\mathcal F,P)
```


와 부분 `\(\sigma\)`-대수


```math
\mathcal G\subseteq\mathcal F
```


가 있다고 하자.

그리고 우선 `\(Y\ge0\)`인 적분가능한 확률변수를 생각하자.

`\(\mathcal G\)` 위에서 새로운 측도 `\(\nu\)`를


```math
\boxed{ \nu(A) = \int_A Y\,dP, \qquad A\in\mathcal G }
```


로 정의한다.

이제 `\(P\)`를 `\(\mathcal G\)`에 제한한 측도를


```math
P|_{\mathcal G}
```


라고 하자.

만약


```math
P(A)=0
```


이면


```math
\nu(A) = \int_A Y\,dP = 0.
```


따라서


```math
\boxed{ \nu\ll P|_{\mathcal G}. }
```


그러면 RN 정리를 사용할 수 있다.

어떤 `\(\mathcal G\)`-가측함수 `\(Z\)`가 존재해서


```math
\nu(A) = \int_AZ\,dP
```


가 모든 `\(A\in\mathcal G\)`에 대해 성립한다.

그런데 `\(\nu\)`의 정의를 대입하면


```math
\boxed{ \int_AZ\,dP = \int_AY\,dP \qquad \forall A\in\mathcal G. }
```


언뜻 보면 `\(Z=Y\)`로 잡으면 끝나는 것 같다. 하지만 `\(Y\)`는 `\(\mathcal F\)`-가측일 뿐 일반적으로 `\(\mathcal G\)`-가측이 아니다. `\(\nu\)`와 `\(P|_{\mathcal G}\)`는 `\(\mathcal G\)` 위의 측도이므로 그 RN derivative도 `\(\mathcal G\)`-가측이어야 하고, `\(Y\)`에게는 그 자격이 없다.

`\(\mathcal G\)`가 주는 정보만으로 만든 함수 중에 이 등식을 만족하는 것이 **존재한다**는 보장, 그것이 RN 정리가 해 주는 일이다.

이 `\(Z\)`가 바로


```math
\boxed{ Z=E[Y\mid\mathcal G]. }
```


다.

일반적인 integrable `\(Y\)`에 대해서는 `\(Y^+,Y^-\)`로 나누거나 signed-measure 버전의 RN 정리를 사용하면 된다.

즉 조건부 기댓값은 갑자기 하늘에서 떨어지는 정의가 아니다.


```math
\boxed{ \text{conditional expectation의 존재} = \text{Radon–Nikodym theorem}. }
```


---

# 22. 마무리

이번 강에서는 우리가 너무 자연스럽게 사용해 온 “밀도”라는 말을 측도론적으로 다시 정의했다.

밀도는 분포 자체에 붙어 있는 함수가 아니다.

항상 기준측도와의 관계다.


```math
\boxed{ \frac{dP}{d\mu}. }
```


그리고 이 함수가 존재하려면


```math
\boxed{ P\ll\mu }
```


여야 한다.

즉 `\(\mu\)`가 `\(0\)`이라고 보는 곳에 `\(P\)` 역시 질량을 놓지 않아야 한다.

반대로


```math
P\perp\mu
```


라면 두 측도는 서로 다른 곳에 산다.

일반적인 측도는 이 둘 중 하나일 필요가 없고, Lebesgue 분해정리에 의해


```math
\boxed{ P=P_{\mathrm{ac}}+P_{\mathrm{s}} }
```


로 나뉜다.

그중 절대연속 부분을 함수 하나로 표현해 주는 것이 RN 정리다.


```math
\boxed{ P\ll\mu \quad\Longrightarrow\quad P(A) = \int_A \frac{dP}{d\mu}\,d\mu. }
```


이 기호를 이해하면 pdf와 pmf가 하나가 된다.


```math
\boxed{ \text{pdf}=\frac{dP}{d\lambda}, \qquad \text{pmf}=\frac{dP}{d\#}. }
```


통계학의 likelihood도 같은 물건이다.


```math
\boxed{ L(\theta;x) = \frac{dP_\theta}{d\mu}(x). }
```


두 확률측도 자체를 비교하면 density ratio


```math
\boxed{ \frac{dP}{dQ} }
```


가 나오고, 이것을 log로 만들어 `\(P\)` 아래에서 평균내면 KL divergence가 된다.


```math
\boxed{ D_{\mathrm{KL}}(P\|Q) = E_P \left[ \log\frac{dP}{dQ} \right]. }
```


반대로 이것을 `\(Q\)` 아래의 가중치로 사용하면 importance sampling이 된다.


```math
\boxed{ E_P[f] = E_Q \left[ f\frac{dP}{dQ} \right]. }
```


따라서 이번 강 전체를 하나의 그림으로 요약하면


```math
\boxed{ \begin{array}{c} P\ll Q\\[2mm] \Downarrow\\[2mm] \dfrac{dP}{dQ}\\[3mm] \swarrow\qquad\downarrow\qquad\searrow\\[2mm] \text{likelihood ratio} \qquad \text{KL} \qquad \text{importance weight} \end{array} }
```


라고 할 수 있다.

그리고 RN 정리의 역할은 여기서 끝나지 않는다.

이번 강에서는

> “한 측도를 다른 측도의 밀도로 표현할 수 있다.”

는 것을 배웠다.

다음 강에서는 이 정리를 한 번 더 사용한다.

확률변수 `\(Y\)`가 만든 측도


```math
A\mapsto\int_A Y\,dP
```


를 정보 `\(\mathcal G\)` 위의 `\(P\)`에 대한 밀도로 표현하면


```math
\boxed{ E[Y\mid\mathcal G] }
```


가 나온다.

그리고 `\(Y\in L^2\)`라면 6강에서 배운 힐베르트 공간의 사영 정리와 다시 만나


```math
\boxed{ E[Y\mid X] = X\text{가 주는 정보로 만들 수 있는 최선의 }L^2\text{ 예측} }
```


이라는 회귀의 언어로 바뀐다.

다음 강에서는 이 연결을 다룬다.

---

## 참고

- Rosenthal, _A First Look at Rigorous Probability Theory_
- Axler, _Measure, Integration & Real Analysis_
- Tao, _An Introduction to Measure Theory_
