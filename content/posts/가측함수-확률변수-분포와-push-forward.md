---
title: "가측함수, 확률변수, 분포와 Push-forward"
date: 2026-08-26
lastmod: 2026-09-03
draft: false
math: true
description: "확률변수가 왜 가측함수여야 하는지에서 출발해, 분포를 push-forward 측도로 정의한다. CDF 하나가 분포 전체를 결정하는 이유, 이산도 연속도 아닌 Cantor 분포, 그리고 역변환 샘플링·reparameterization trick·normalizing flow·GAN이 모두 같은 push-forward라는 것까지 정리한다."
vault_source: "Atlas/가측함수, 확률변수, 분포와 Push-forward.md"
---

앞에서는 확률공간


```math
(\Omega, \mathcal{F}, P)
```


을 만들었다.

- `\(\Omega\)`: 실제로 일어날 수 있는 결과들
- `\(\mathcal{F}\)`: 우리가 구별할 수 있는 사건들
- `\(P\)`: 각 사건에 부여된 확률

그런데 실제 확률론이나 머신러닝에서 우리가 직접 다루는 것은 보통 `\(\omega \in \Omega\)` 자체가 아니다.

동전을 100번 던졌을 때 정확히 어떤 앞뒤 배열이 나왔는지보다 **앞면이 몇 번 나왔는지**가 궁금할 수 있고, 사람 한 명이라는 복잡한 결과 전체보다 **키가 몇 cm인지**만 관심 있을 수도 있다.

즉 복잡한 결과 `\(\omega\)`에서 우리가 관심 있는 숫자를 뽑아내는 함수


```math
X : \Omega \to \mathbb{R}
```


를 생각하게 된다.

확률론에서는 이런 함수를 **가측함수**(measurable function)라고 부른다. 그리고 확률변수(random variable)란 바로 이 가측함수다.


```math
\boxed{\text{확률변수} = \text{가측함수(measurable function)}}
```


이번 글에서는 왜 가측성이 필요한지에서 출발해,


```math
\boxed{
\text{가측함수}
\longrightarrow \text{확률변수}
\longrightarrow \text{push-forward}
\longrightarrow \text{분포}
\longrightarrow \text{CDF}
}
```

라는 흐름을 설명하겠다.

---

# 요약


```math
\boxed{
(\Omega, \mathcal{F}, P)
\;\xrightarrow{\ X\ \text{가측}\ }\;
(\mathbb{R}, \mathcal{B}(\mathbb{R}), P_X),
\qquad
P_X(B) = P(X^{-1}(B))
}
```


- **가측함수**: `\(B \in \mathcal{S} \Rightarrow X^{-1}(B) \in \mathcal{F}\)`. 도착공간에서 물어볼 수 있는 질문을 원래 공간의 사건으로 되돌릴 수 있어야 한다. 역상이라서 집합연산이 보존되고, 확인은 생성집합에서만 하면 된다 (0~5절)
- **확률변수**: 실수값 가측함수. 변수가 아니라 함수이고, 랜덤한 것은 입력 `\(\omega\)`다 (6~7절)
- **분포 = push-forward**: `\(P_X = X_{\#}P\)`. `\(X\)`는 결과를 값으로 옮기는 동시에 확률측도를 실수축으로 밀어낸다 (8~10절)
- **CDF**: `\(F_X(x) = P_X((-\infty, x])\)`. 반직선에서의 값만으로 `\(P_X\)` 전체가 결정된다 (11절)
- 분포가 같다고 확률변수가 같은 건 아니다 (12절)
- 분포에는 이산, 연속도 아닌 것이 있다 (13절)
- **ML 응용**: 간단한 분포 `\(+\)` 가측함수 `\(\to\)` 원하는 분포. 예시 역변환 샘플링·reparameterization trick·normalizing flow·GAN (14~17절)
- **`\(\sigma(X)\)`**: `\(\{X^{-1}(B) : B \in \mathcal{B}(\mathbb{R})\}\)` = `\(X\)`의 값만 보고 판별할 수 있는 사건들 = `\(X\)`가 주는 정보. `\(E[Y \mid X] = E[Y \mid \sigma(X)]\)`로 이어진다 (18~20절)
- 목적지는 `\(\mathbb{R}\)`일 필요가 없다. `\((M, \mathcal{B}(M))\)`이면 되고, 그때는 확률변수가 아니라 확률원소다 (21절)

---

# 0. 왜 함수에 조건이 필요한가?

동전을 두 번 던진다고 하자.


```math
\Omega = \{HH, HT, TH, TT\}.
```


우리는 앞면의 개수만 알고 싶다고 하자.


```math
X(HH) = 2, \qquad X(HT) = X(TH) = 1, \qquad X(TT) = 0.
```


그러면


```math
X : \Omega \to \mathbb{R}
```


이다.

이제

> “앞면이 한 번 이하 나왔을 확률은?”

이라고 물으면


```math
P(X \le 1)
```


을 계산하고 싶다.

그런데 `\(P\)`는 `\(\mathbb{R}\)`의 집합에 확률을 주는 함수가 아니다.

원래


```math
P : \mathcal{F} \to [0, 1]
```


이므로 `\(\Omega\)` 안의 사건에만 확률을 줄 수 있다.

그래서


```math
\{X \le 1\}
```


을 `\(\Omega\)`의 사건으로 바꿔야 한다.


```math
\begin{aligned}
\{X \le 1\}
&= \{\omega \in \Omega : X(\omega) \le 1\} \\
&= X^{-1}((-\infty, 1]).
\end{aligned}
```


이 예에서는


```math
X^{-1}((-\infty, 1]) = \{HT, TH, TT\}.
```


따라서


```math
P(X \le 1) = P(\{HT, TH, TT\})
```


라고 계산할 수 있다.

여기서 중요한 문제가 나온다.

> 만약 `\(X^{-1}((-\infty, 1])\)`가 `\(\mathcal{F}\)`에 들어 있지 않다면?

그러면 그 집합에 `\(P\)`를 적용할 수 없다.

즉


```math
P(X \le 1)
```


이라는 표현 자체가 정의되지 않는다.

그래서 확률변수로 사용할 함수는 적어도 우리가 도착공간에서 물어보는 사건들을 원래 확률공간의 사건으로 끌고 올 수 있어야 한다.

이 조건이 바로 **가측성**(measurability)이다.

---

# 1. 가측함수의 정의

두 측정공간


```math
(\Omega, \mathcal{F}), \qquad (S, \mathcal{S})
```


가 있다고 하자.

함수


```math
X : \Omega \to S
```


가 **가측함수**(measurable function)라는 것은


```math
\boxed{
B \in \mathcal{S}
\quad \Rightarrow \quad
X^{-1}(B) \in \mathcal{F}
}
```


라는 뜻이다.

즉 `\(S\)`에서 측정 가능한 모든 집합을 `\(X\)`를 통해 역상으로 끌어왔을 때, 그것이 `\(\Omega\)`에서도 측정 가능해야 한다.

실수값 함수라면 보통


```math
X : (\Omega, \mathcal{F}) \to (\mathbb{R}, \mathcal{B}(\mathbb{R}))
```


를 생각하므로


```math
\boxed{
B \in \mathcal{B}(\mathbb{R})
\ \Rightarrow\
X^{-1}(B) \in \mathcal{F}
}
```


이면 된다.

만일 함수 `\(X\)`가 가측이 아니게 되면

```math
P(X \in B)
```

이와 같은 표현이 의미를 가지지 못하게 되므로 가측성은 중요하다.

---

# 2. 그런데 왜 하필 역상(preimage)인가?

처음 보면 조금 이상하다.

함수는


```math
X : \Omega \to \mathbb{R}
```


처럼 앞으로 가는데, 정의에서는 왜


```math
X^{-1}(B)
```


처럼 거꾸로 돌아오는 걸까?

이유는 간단하다.

**측도 `\(P\)`가 정의되어 있는 곳이 `\(\Omega\)`이기 때문이다.**

우리가


```math
B \subseteq \mathbb{R}
```


라는 사건에 관심 있다고 하자.

예를 들어


```math
B = [170, \infty)
```


라면

> “키가 170cm 이상이다.”

라는 질문이다.

그런데 확률 `\(P\)`는 사람의 키 공간 `\(\mathbb{R}\)`에 직접 정의되어 있는 것이 아니라 원래 표본공간 `\(\Omega\)`에 정의되어 있다.

따라서


```math
X^{-1}([170, \infty)) = \{\omega : X(\omega) \ge 170\}
```


로 질문을 원래 공간으로 가져와야 한다.

그러면 비로소


```math
P(X \ge 170) = P(X^{-1}([170, \infty)))
```


를 계산할 수 있다.

따라서 가측성을 정보의 관점에서 보면


```math
\boxed{
\begin{array}{c}
\text{도착공간에서 할 수 있는 질문을} \\
\text{원래 공간에서도 사건으로 해석할 수 있다}
\end{array}
}
```


는 조건이다.

---

# 3. 그래서 어떤 함수가 가측인가?

정의를 봤으니 자연스러운 질문이 따라온다.

> 내가 실제로 쓰는 함수는 가측인가?

만약 매번 모든 Borel 집합 `\(B\)`에 대해


```math
X^{-1}(B) \in \mathcal{F}
```


를 확인해야 한다면 확률론은 시작조차 못 할 것이다.

다행히 결론은 **거의 항상 가측이다**.

> 연속함수가 가측이라는 사실은 증명 없이 넘어가겠다. 열린집합을 이용한 연속함수의 정의를 쓰면 바로 나온다.

| 함수                                          | 가측인 이유                                 |
| ------------------------------------------- | -------------------------------------- |
| 다항함수, `\(e^x\)`, `\(\log x\)`, `\(\sin x\)`             | 연속                                     |
| ReLU, sigmoid, tanh, softmax                | 연속                                     |
| 신경망                                         | 연속함수의 합성                               |
| 계단함수, 구간별 연속함수                              | 각 조각이 가측이고 유한 합집합                      |
| 지시함수 `\(\mathbf{1}_A\)` (단 `\(A \in \mathcal{F}\)`) | 역상이 `\(\emptyset, A, A^{c}, \Omega\)` 중 하나 |
| 단조함수                                        | `\(\{f \le a\}\)`가 항상 구간 (아래 5절의 판정법)      |
| 위 함수들의 합, 곱, 합성, 극한                         | 4절에서 볼 연산 안정성                          |

마지막 줄이 특히 중요하다.

4절에서 보겠지만 가측함수는 사칙연산, 합성, `\(\sup\)`, `\(\inf\)`, 극한에 대해 모두 닫혀 있다.

그래서


```math
\boxed{\text{가측인 재료로 정상적인 조립을 하면 결과도 자동으로 가측이다}}
```


물론 가측이 아닌 함수도 존재하지만 여기서는 넘어가도록 하자.

---

# 4. 가측함수는 연산에 강하다

가측함수는 생각보다 쉽게 만들어진다.

`\(X, Y : \Omega \to \mathbb{R}\)`가 가측이라면 보통


```math
X + Y, \qquad X - Y, \qquad XY, \qquad |X|, \qquad \max(X, Y), \qquad \min(X, Y)
```


도 모두 가측이다.

또한


```math
X_n(\omega) \to X(\omega)
```


이고 모든 `\(X_n\)`이 가측이라면 그 점별극한 `\(X\)`도 가측이다.

더 일반적으로


```math
\sup_n X_n, \qquad \inf_n X_n, \qquad \limsup_n X_n, \qquad \liminf_n X_n
```


역시 가측이다.

이 성질은 굉장히 중요하다.

확률론에서는 함수열의 극한을 끝없이 다루기 때문이다.

그래서 실제 수학을 하다 보면

> “이 함수 가측 맞나?”

를 매 순간 걱정하기보다는, 이미 알고 있는 가측함수들을 정상적인 방식으로 조합했다면 대부분 자동으로 가측이 된다.

거칠게 기억한다면


```math
\boxed{\text{웬만한 정상적인 함수는 가측이다}}
```


정도로 생각해도 좋다.

---

# 5. 모든 Borel 집합을 확인해야 하나?

정의만 보면 가측성을 확인하려면


```math
X^{-1}(B) \in \mathcal{F}
\qquad \forall B \in \mathcal{B}(\mathbb{R})
```


모든 Borel 집합의 역상이 `\(\mathcal{F}\)`에 들어감을 일일이 확인해야 할 것처럼 보인다.

하지만 그럴 필요는 없다.

결론만 말하자면 Borel σ-대수는


```math
\{(-\infty, a] : a \in \mathbb{R}\}
```


만으로 생성되므로 실수값 함수 `\(X\)`에 대해서는


```math
\boxed{
\{\omega : X(\omega) \le a\} \in \mathcal{F}
\qquad \forall a \in \mathbb{R}
}
```


만 확인해도 `\(X\)`가 가측이라는 것을 알 수 있다.

즉


```math
\boxed{
X \text{ measurable}
\iff
\{X \le a\} \in \mathcal{F} \quad \forall a \in \mathbb{R}
}
```


라고 생각해도 된다.

확률론에서


```math
P(X \le x)
```


라는 형태가 계속 등장하는 이유와도 잘 연결된다.(CDF가 위와 같은 형태이다.)

## 위 논증의 추가 설명

> 생성원에서만 확인해도 왜 Borel 집합 전체가 따라오는지, 그 틈을 무엇이 메우는지가 궁금하지 않다면 건너뛰어도 좋다. 위의 결론만으로 다음 절로 넘어가는 데 지장은 없다.

사실 위와 같은 논증은 자명하지 않다. 생성원에서 `\(X^{-1}(B) \in \mathcal{F}\)`가 성립한다고 해서, 거기서 만들어지는 Borel 집합에 대해서도 성립한다는 보장이 저절로 따라오지는 않는다.

이 틈을 메우는 것이 다음 사실이다.


```math
\boxed{
\mathcal{A} = \{B \subseteq \mathbb{R} : X^{-1}(B) \in \mathcal{F}\}
\ \text{는 } \sigma\text{-대수}
}
```


**역상이 집합 연산과 교환되기 때문**이다.


```math
X^{-1}(B^{c}) = \big(X^{-1}(B)\big)^{c},
\qquad
X^{-1}\Big(\bigcup_{n} B_n\Big) = \bigcup_{n} X^{-1}(B_n)
```


즉 `\(\mathcal{A}\)` 안에서 여집합을 취하거나 가산합집합을 만들어도 결과는 여전히 `\(\mathcal{F}\)` 안에 남는다.

이제 생성원 `\(\mathcal{G} = \{(-\infty, a] : a \in \mathbb{R}\}\)`가 `\(\mathcal{A}\)`에 들어 있다고 하자. `\(\sigma(\mathcal{G})\)`는 `\(\mathcal{G}\)`를 포함하는 **가장 작은** σ-대수인데 `\(\mathcal{A}\)` 역시 `\(\mathcal{G}\)`를 포함하는 σ-대수이므로


```math
\mathcal{B}(\mathbb{R}) = \sigma(\mathcal{G}) \subseteq \mathcal{A}
```


가 되어, 모든 Borel 집합 원소가 `\(\mathcal{A}\)`에 들어가고 따라서 역상이 `\(\mathcal{F}\)`에 들어간다.

그런데 방금 논증을 다시 읽어보면 눈에 띄는 점이 있다.

`\(\mathbb{R}\)`의 성질도, Borel 집합의 성질도 **한 번도 쓰지 않았다.** 쓴 것은 역상이 여집합·가산합집합과 교환된다는 것, 그리고 `\(\sigma(\mathcal{G})\)`가 최소라는 것뿐이다.

그래서 `\(\mathbb{R}\)`을 임의의 측정공간으로 바꿔도 논증이 한 글자도 달라지지 않는다.


```math
\boxed{
\mathcal{S} = \sigma(\mathcal{G})
\quad\text{일 때}\quad
X^{-1}(G) \in \mathcal{F} \ \ (\forall G \in \mathcal{G})
\ \Longrightarrow\
X : (\Omega, \mathcal{F}) \to (S, \mathcal{S}) \text{ 가측}
}
```


즉 **생성원만 확인하면 된다**는 것은 σ-대수 일반의 성질이다.

| 목표공간 `\(S\)`       | 생성원 `\(\mathcal{G}\)`  | 확인할 것                         |
| -------------- | ------------------ | ----------------------------- |
| `\(\mathbb{R}\)`   | `\(\{(-\infty, a]\}\)` | `\(\{X \le a\} \in \mathcal{F}\)` |
| `\(\mathbb{R}^n\)` | 열린 상자              | 각 좌표 `\(X_i\)`가 가측                |
| 위상공간           | 열린집합               | 열린집합의 역상이 `\(\mathcal{F}\)`에 속함   |

> 이런 논법을 좋은 집합 원리(good sets principle)라고 한다. 상(image)은 여집합과 교환되지 않아 같은 논법이 통하지 않는다. 2절에서 역상을 택한 이유가 여기서 한 번 더 확인되는 셈이다. 그리고 21절에서 push-forward의 목적지를 `\(S^2\)`나 `\(SO(3)\)` 같은 manifold로 옮길 수 있는 것도 이 성질 덕분이다.

---

# 6. 확률변수 = 가측함수

이제 확률공간


```math
(\Omega, \mathcal{F}, P)
```


가 있다고 하자.

실수값 함수


```math
X : \Omega \to \mathbb{R}
```


가


```math
(\mathcal{F}, \mathcal{B}(\mathbb{R}))
```


에 대해 가측이면 `\(X\)`를 **확률변수**(random variable)라고 한다.

즉


```math
\boxed{
X : \Omega \to \mathbb{R} \text{ measurable}
}
```


이면 확률변수다.

여기서 이름 때문에 약간 혼란스러울 수 있다.

확률변수는 사실 **변수라기보다 함수**다.


```math
\boxed{\text{random variable은 function이다}}
```


랜덤한 것은 함수 `\(X\)` 자체가 아니라 입력되는


```math
\omega \sim P
```


이다.


```math
\omega \overset{X}{\longmapsto} X(\omega)
```


에서 `\(\omega\)`가 어떤 값이 될지 모르기 때문에 결과 `\(X(\omega)\)`도 랜덤하게 보이는 것이다.

---

# 7. 확률변수는 복잡한 세계를 숫자로 요약한다

동전을 두 번 던지는 예로 돌아가자.


```math
\Omega = \{HH, HT, TH, TT\}
```


이고


```math
X(\omega) = \text{앞면의 개수}
```


라고 하자.

그러면


```math
X(HH) = 2, \qquad X(HT) = X(TH) = 1, \qquad X(TT) = 0.
```


원래 표본공간에는 네 가지 결과가 있었지만 `\(X\)`를 통해 보면


```math
0, \quad 1, \quad 2
```


세 가지 값만 남는다.

특히


```math
HT, \quad TH
```


는 서로 다른 결과인데도


```math
X(HT) = X(TH) = 1
```


이므로 `\(X\)`만 관측해서는 둘을 구별할 수 없다.

확률변수는 원래 세계의 모든 정보를 보존하는 것이 아니다.

우리가 관심 있는 정보를 뽑아내는 **관측 장치**라고 보는 것이 좋다.

---

# 8. 확률변수의 분포는 어디서 오는가?

이제 핵심이다.

우리가


```math
X \sim N(0, 1)
```


이라고 말할 때 이 정규분포는 대체 어디서 나온 것일까?

원래 확률은


```math
P
```


라는 형태로 `\(\Omega\)` 위에 있었다.

그런데 `\(X\)`가


```math
\Omega \to \mathbb{R}
```


로 결과들을 실수축으로 보내고 있다.

따라서 `\(\Omega\)` 위에 존재하던 확률측도 `\(P\)`도 `\(X\)`를 따라서 `\(\mathbb{R}\)`로 이동시킬 수 있다.

실수축의 Borel 집합


```math
B \in \mathcal{B}(\mathbb{R})
```


에 대해


```math
P_X(B) = P(X \in B)
```


라고 정의한다.

그런데


```math
\{X \in B\} = X^{-1}(B)
```


이므로


```math
\boxed{
P_X(B) = P(X^{-1}(B))
}
```


이다.

이를 함수 합성처럼 쓰면


```math
\boxed{
P_X = P \circ X^{-1}
}
```


이다.

이 `\(P_X\)`를 `\(X\)`의 **분포**(distribution, law)라고 한다.

처음의 질문으로 돌아가면, `\(X \sim N(0, 1)\)`이라는 말은


```math
\boxed{N(0, 1) = P_X = P \circ X^{-1}}
```


이라는 뜻이다. 즉 **정규분포는 확률측도 `\(P\)`를 `\(X\)`를 따라 실수축으로 이동시킨 결과물**이다.

---

# 9. Push-forward

위 과정을 측도론에서는 **push-forward**라고 부른다.

일반적으로 측도공간


```math
(\Omega, \mathcal{F}, \mu)
```


와 가측함수


```math
T : \Omega \to S
```


가 있으면 `\(T\)`를 통해 `\(S\)` 위에 새로운 측도를 만들 수 있다.


```math
\boxed{
T_{\#}\mu(B) = \mu(T^{-1}(B))
}
```


이를 `\(\mu\)`의 `\(T\)`에 의한 push-forward라고 한다.

기호는


```math
T_{\#}\mu
```


를 많이 사용한다.

확률변수에서는


```math
\boxed{
P_X = X_{\#}P
}
```


이다.

그림으로 보면


```math
(\Omega, \mathcal{F}, P)
\overset{X}{\longrightarrow}
(\mathbb{R}, \mathcal{B}(\mathbb{R}), P_X).
```


즉

> **확률변수는 표본을 실수로 보내는 동시에, 원래 확률측도를 실수축 위의 분포로 밀어낸다.**

---

# 10. 간단한 push-forward 예


```math
\Omega = [0, 1], \qquad P = \operatorname{Unif}[0, 1]
```


이라고 하자.

그리고


```math
X(\omega) = \omega^2
```


라고 하자.

그러면 `\(X\)`가 만드는 분포 `\(P_X\)`를 알고 싶다.

`\(0 \le x \le 1\)`에서


```math
\begin{aligned}
P_X((-\infty, x])
&= P(X \le x) \\
&= P(\omega^2 \le x) \\
&= P(\omega \le \sqrt{x}) \\
&= \sqrt{x}.
\end{aligned}
```


따라서 `\(X\)`의 분포는


```math
P_X((-\infty, x]) = \sqrt{x}, \qquad 0 \le x \le 1
```


로 완전히 결정된다. 미분하면 밀도는


```math
p_X(x) = \frac{1}{2\sqrt{x}}, \qquad 0 < x < 1.
```


원래 균등했던 확률측도가


```math
\omega \mapsto \omega^2
```


에 의해 실수축 위에서 재배치된 것이다.

이것이 push-forward다.

---

# 11. CDF는 분포를 압축해서 표현한다

실수값 확률변수 `\(X\)`에 대해


```math
\boxed{
F_X(x) = P(X \le x)
}
```


를 누적분포함수(CDF)라고 한다.

push-forward를 사용하면


```math
F_X(x) = P_X((-\infty, x]).
```


즉 CDF는 `\(P_X\)`가 특정한 형태의 집합


```math
(-\infty, x]
```


에 얼마의 확률을 주는지를 기록한 함수다.

처음 보면 의문이 생긴다.

> 분포 `\(P_X\)`는 모든 Borel 집합에 확률을 주는데,
> CDF는 `\((-\infty, x]\)` 같은 집합만 보고 있다.
> 정말 이것만으로 전체 분포를 알 수 있을까?

놀랍게도 그렇다.


```math
\boxed{\text{CDF 하나는 실수 위의 확률분포를 완전히 결정한다.}}
```


왜냐하면 생성원


```math
\{(-\infty, x] : x \in \mathbb{R}\}
```


에서 일치하는 두 확률측도는 전체 Borel σ-대수에서도 일치하기 때문이다.

다만 이것은 5절의 논법이 그대로 적용된 결과가 아니다. 아래에서 따로 다룬다.

따라서


```math
F_X = F_Y
```


이면


```math
P_X = P_Y.
```


즉


```math
\boxed{
\text{CDF가 같다} \iff \text{분포가 같다}
}
```


라고 생각할 수 있다.

## 위 논증의 추가 설명

> CDF 하나가 왜 분포 전체를 결정하는지, 그 증명에 왜 π-λ 정리까지 필요한지가 궁금하지 않다면 건너뛰어도 좋다. 위의 결론만으로 다음 절로 넘어가는 데 지장은 없다.

### 문제를 어떤 모양으로 바꿔야 하는가

보여야 할 것은


```math
F_X = F_Y
\ \Longrightarrow\
P_X = P_Y
```


인데, 이 식의 두 변이 말하는 범위가 서로 크게 다르다는 점부터 봐야 한다.

|                | 실제로 주장하는 것                                                        |
| -------------- | ----------------------------------------------------------------- |
| 가정 `\(F_X = F_Y\)` | 모든 `\(x \in \mathbb{R}\)`에 대해 `\(P_X((-\infty, x]) = P_Y((-\infty, x])\)` |
| 결론 `\(P_X = P_Y\)` | **모든** Borel 집합 `\(B\)`에 대해 `\(P_X(B) = P_Y(B)\)`                         |

가정은 `\((-\infty, x]\)` 꼴의 집합에 대해서만 말하는데 결론은 Borel 집합 전체를 요구한다. 그런데 Borel 집합은 열거할 수 있는 대상이 아니므로, `\(B\)`를 하나씩 꺼내 확인하는 길은 처음부터 막혀 있다.

5절에서 똑같은 곤란을 겪었고, 그때 쓴 방법이 **좋은 집합 원리**였다. 원하는 성질이 성립하는 집합들을 한데 모아놓고 그 **모임의 구조**를 따지는 것이다. 여기서도 그대로 한다. 이번에 좋은 집합은 **두 측도가 일치하는 집합**이다.


```math
\mathcal{D} = \{B \in \mathcal{B}(\mathbb{R}) : P_X(B) = P_Y(B)\}
```


이렇게 두면 가정과 결론이 **둘 다 `\(\mathcal{D}\)`에 대한 포함관계**로 번역된다.

|                | 포함관계로                                                                     |
| -------------- | ------------------------------------------------------------------------- |
| 가정 `\(F_X = F_Y\)` | `\(\mathcal{G} = \{(-\infty, x] : x \in \mathbb{R}\} \subseteq \mathcal{D}\)` |
| 결론 `\(P_X = P_Y\)` | `\(\mathcal{B}(\mathbb{R}) \subseteq \mathcal{D}\)`                           |

그리고 `\(\mathcal{B}(\mathbb{R}) = \sigma(\mathcal{G})\)`이므로 증명해야 할 것은 결국


```math
\boxed{
\mathcal{G} \subseteq \mathcal{D}
\ \Longrightarrow\
\sigma(\mathcal{G}) \subseteq \mathcal{D}
}
```


하나로 줄어든다. 확률 계산 문제가 **집합족의 구조 문제**로 바뀐 것이다.

만일 `\(\mathcal{D}\)`가 σ-대수라면, `\(\sigma(\mathcal{G})\)`가 `\(\mathcal{G}\)`를 포함하는 **가장 작은** σ-대수라는 사실로부터 증명이 바로 끝난다. 하지만 이번에는 그 길이 막혀 있다.

### `\(\mathcal{D}\)`는 σ-대수가 아니다

시도해보면 막힌다.

5절에서 그 수가 통했던 것은


```math
\mathcal{A} = \{B : X^{-1}(B) \in \mathcal{F}\}
```


의 경우 **역상이 여집합·가산합집합과 교환**되어 `\(\mathcal{A}\)`가 σ-대수임이 곧바로 나왔기 때문이다. 그런데 지금 `\(\mathcal{D}\)`에는 역상이 없다. 무엇이 되고 무엇이 안 되는지 직접 확인해보자.

| 연산 | 성립? | 이유 |
| --- | --- | --- |
| `\(\mathbb{R} \in \mathcal{D}\)` | ✓ | `\(P_X(\mathbb{R}) = P_Y(\mathbb{R}) = 1\)` |
| 여집합 | ✓ | `\(P_X(B^{c}) = 1 - P_X(B) = 1 - P_Y(B) = P_Y(B^{c})\)` |
| **서로소** 가산합집합 | ✓ | `\(P_X(\bigsqcup_{n} B_n) = \sum_{n} P_X(B_n) = \sum_{n} P_Y(B_n)\)` |
| 일반 가산합집합 | ✗ | 아래 |

마지막 줄이 문제다.


```math
P_X(A \cup B) = P_X(A) + P_X(B) - P_X(A \cap B)
```


에서 보듯 합집합의 확률에는 **교집합 항이 끼어든다.** `\(A\)`와 `\(B\)`에서 두 측도가 일치한다는 것만으로는 `\(A \cap B\)`에서 일치한다는 보장이 없고, 따라서 `\(A \cup B\)`에서 일치한다는 결론도 따라오지 않는다.

여집합과 서로소 가산합집합에만 닫힌 이런 집합족을 **λ-체계(Dynkin system)**라고 한다.

정리하면 이렇다.

|                   | 얻은 것 | 모자란 것    |
| ----------------- | ---- | -------- |
| 5절의 `\(\mathcal{A}\)` | σ-대수 | —        |
| 지금의 `\(\mathcal{D}\)` | λ-체계 | 일반 가산합집합 |

`\(\mathcal{D}\)`에서 더 받아낼 것은 없다. 그렇다면 모자란 만큼을 **반대쪽에서**, 즉 생성원 `\(\mathcal{G}\)` 쪽에서 지불하는 수밖에 없다. 그리고 방금 본 대로 정보가 새는 지점이 교집합이었으므로, 요구해야 할 조건도 짐작이 된다.

### π-λ 정리

유한교집합에 닫힌 집합족을 **π-체계**라고 한다. 틈을 메우는 것이 다음 사실이다.


```math
\boxed{
\mathcal{G} \text{ 가 } \pi\text{-체계},
\quad
\mathcal{D} \supseteq \mathcal{G} \text{ 가 } \lambda\text{-체계}
\ \Longrightarrow\
\sigma(\mathcal{G}) \subseteq \mathcal{D}
}
```


이것을 **π-λ 정리** 또는 Dynkin의 보조정리라고 한다. λ-체계라는 약한 구조에서 출발하더라도, 생성원 쪽에 **π-체계** 조건을 얹어주면 σ-대수일 때와 똑같은 결론에 도달할 수 있다는 뜻이다.

> 증명은 생략한다.

이제 우리 생성원이 π-체계인지만 확인하면 된다.


```math
(-\infty, x] \cap (-\infty, y] = (-\infty, x \wedge y]
```


두 반직선의 교집합은 다시 반직선이다. 조건이 충족된다.


---

# 12. 그런데 분포가 같다고 확률변수가 같은 것은 아니다

여기서 중요한 구별이 있다.


```math
\boxed{ X = Y }
```


와


```math
\boxed{ X \overset{d}{=} Y }
```


는 완전히 다른 말이다.

예를 들어


```math
X \sim N(0, 1)
```


이라고 하자.

그러면 정규분포의 대칭성 때문에


```math
-X \sim N(0, 1)
```


이다.

따라서


```math
\boxed{ X \overset{d}{=} -X }
```


이다.

하지만 일반적으로


```math
X(\omega) \neq -X(\omega)
```


이므로 두 함수 자체가 같은 것은 아니다.

즉


```math
\boxed{
\text{확률변수} \quad \neq \quad \text{확률변수의 분포}
}
```


이다.

확률변수는


```math
X : \Omega \to \mathbb{R}
```


라는 함수이고,

분포는


```math
P_X
```


라는 `\(\mathbb{R}\)` 위의 측도다.

서로 다른 함수들이 똑같은 분포를 만들어낼 수 있다.

---

# 13. 이산분포와 연속분포만 있는 것은 아니다

확률분포를 처음 배우면 보통 두 종류를 배운다.


```math
P(X = x_i) = p_i
\qquad\text{또는}\qquad
P(X \in A) = \int_A p(x) \, dx
```


그래서 모든 분포가 둘 중 하나일 것처럼 느껴진다. 하지만 그렇지 않다.


```math
\boxed{
\text{distribution} \;\supsetneq\; \{\text{discrete}\} \cup \{\text{density}\}
}
```


두 용어를 짚고 가자. 사실 방금 쓴 두 식이 그대로 정의다.

| 용어 | 뜻 | 위 식에서 |
| --- | --- | --- |
| **원자**(atom) | `\(P_X(\{x\}) > 0\)` 인 점 `\(x\)` | `\(P(X = x_i) = p_i\)` 의 각 `\(x_i\)` |
| **Lebesgue 밀도** | `\(P_X(A) = \int_A p(x)\,dx\)` 를 만족하는 함수 `\(p\)` | 적분 안의 `\(p(x)\)` |

그러면 위의 두 종류를 이렇게 다시 쓸 수 있다. 이산분포는 **원자만으로** 이루어진 분포이고, 연속분포는 **밀도를 가진** 분포다. 정확히는 후자를 **절대연속**(absolutely continuous)이라고 부른다. 따라서 원자도 없고 밀도도 없는 분포는 둘 중 **어느 쪽도 아니다.**

그런 분포가 실제로 존재한다. 대표적인 예가 Cantor 분포다.

> **용어 주의.** “연속분포”라는 말은 문맥에 따라 두 가지로 쓰인다. 여기서처럼 **밀도를 가진다**(절대연속)는 뜻일 때도 있고, 단순히 **원자가 없다**(CDF가 연속)는 뜻일 때도 있다. Cantor 분포는 뒤쪽 의미로는 연속이지만 앞쪽 의미로는 아니다. 이렇게 원자도 없고 밀도도 없는 분포를 **특이연속**(singular continuous)이라고 하며, 실수 위의 모든 분포가 이산·절대연속·특이연속 세 조각의 합으로 유일하게 분해된다는 것이 **Lebesgue 분해정리**다.

지금까지 분포를 push-forward 측도


```math
P_X(B) = P(X^{-1}(B))
```


로 정의해온 이유가 여기에 있다. 차이는 **무엇 위의 함수인가**다.

pmf와 pdf는 **점**마다 숫자를 붙여둔 것이다. 집합의 확률은 거기서 `\(\sum_{x_i \in A} p_i\)`나 `\(\int_A p(x)\,dx\)`로 **복원**해야 한다. 반면 `\(P_X\)`는 처음부터 **집합** `\(B\)`에 값을 준다. 복원 단계가 없다.

그리고 그 복원이 늘 가능하지는 않다. Cantor 분포가 그렇다.

**Cantor 집합** `\(C\)` 위에 놓인 이 분포는


```math
P_X(\{x\}) = 0 \ \ (\forall x),
\qquad
P_X(C) = 1
```


을 만족한다. **점마다 보면 전부 0인데 집합으로 보면 1이다.** 점별 정보는 항등적으로 0이니 거기서 복원할 수 있는 것은 아무것도 없다.

밀도가 없다는 것도 여기서 바로 나온다. `\(C\)`는 `\(\operatorname{Leb}(C) = 0\)`인 집합이므로, 만약 밀도 `\(p\)`가 존재했다면


```math
P_X(C) = \int_C p(x)\,dx = 0
```


이어야 하는데 실제 값은 1이다.

즉 점 위의 함수로는 담을 수 없는 정보가 집합 위의 함수에는 남아 있다. 확률을 애초에 집합 위에서 정의한 이유가 이것이다.

> **ML 예시.** 저차원 latent `\(z \in \mathbb{R}^{d}\)`를 생성자 `\(G\)`로 고차원 `\(\mathbb{R}^{D}\)` (`\(d \ll D\)`)에 밀어내면, `\(G_{\#}P_z\)`는 `\(\mathbb{R}^{D}\)` 안의 `\(d\)`차원 집합에 확률을 몰아준다. 이 분포에는 Lebesgue 밀도가 **없다.** GAN에서 우도(likelihood)를 직접 쓰지 못하는 이유가 이것이다.
>
> 16절의 normalizing flow가 굳이 **가역**함수만 쓰는 것도 같은 이유다. 차원을 보존하면서 가역이면 밀도가 다시 밀도로 옮겨가고, 그 변화를 Jacobian으로 추적할 수 있다.

## Cantor 분포에 대한 추가 설명

> `\(C\)`가 어떤 집합인지, 길이가 0인데 어떻게 확률이 1일 수 있는지, 그런 분포를 실제로 어떻게 만드는지가 궁금하지 않다면 건너뛰어도 좋다. 위의 결론만으로 다음 절로 넘어가는 데 지장은 없다.

**Cantor 집합** `\(C\)`는 `\([0,1]\)`에서 **열린** 가운데 `\(1/3\)`을 아래와 같이

| 단계 | 시작 | 파낼 구간 | 남는 것 | 총 길이 |
| --- | --- | --- | --- | --- |
| 1 | `\([0,1]\)` | `\((\tfrac13, \tfrac23)\)` | `\([0,\tfrac13] \cup [\tfrac23,1]\)` | `\(2 \times \tfrac13 = \tfrac23\)` |
| 2 | `\([0,\tfrac13] \cup [\tfrac23,1]\)` | `\((\tfrac19,\tfrac29),\ (\tfrac79,\tfrac89)\)` | `\([0,\tfrac19] \cup [\tfrac29,\tfrac13] \cup [\tfrac23,\tfrac79] \cup [\tfrac89,1]\)` | `\(4 \times \tfrac19 = \tfrac49\)` |
| 3 | 위의 4개 구간 | `\((\tfrac1{27},\tfrac2{27}),\ (\tfrac7{27},\tfrac8{27}),\ (\tfrac{19}{27},\tfrac{20}{27}),\ (\tfrac{25}{27},\tfrac{26}{27})\)` | 8개 구간 | `\(8 \times \tfrac1{27} = \tfrac8{27}\)` |
| `\(n\)` | `\(2^{n-1}\)`개 구간 | 각 구간의 가운데 `\(1/3\)` (`\(2^{n-1}\)`개) | `\(2^{n}\)`개 구간 | `\(2^{n} \times 3^{-n} = (\tfrac23)^{n}\)` |

무한히 반복하고 남은 것이다. 총 길이가 `\((2/3)^{n} \to 0\)`이므로


```math
\operatorname{Leb}(C) = 0
```


이다.

그런데 `\(C\)`는 비어 있지 않다. **열린** 구간만 파냈으므로 `\(0,\ 1,\ \tfrac13,\ \tfrac23,\ \tfrac19,\ \ldots\)` 같은 끝점은 전부 살아남는다. 그리고 끝점만 남는 것도 아니다.

구조는 **3진 전개**로 보면 선명해진다. `\(x \in [0,1]\)`을


```math
x = 0.d_1 d_2 d_3 \cdots_{(3)} = \sum_{n=1}^{\infty} \frac{d_n}{3^{n}},
\qquad d_n \in \{0,1,2\}
```


로 쓰자. 첫 단계에서 파내는 `\((\tfrac13, \tfrac23)\)`은 정확히 `\(d_1 = 1\)`인 수들이다. 둘째 단계에서 파내는 두 구간은 `\(d_2 = 1\)`인 수들이고, 이후도 마찬가지다. 따라서


```math
\boxed{
C = \{\,x \in [0,1] : \text{3진 전개에 숫자 } 1 \text{ 을 쓰지 않는 } x \,\}
}
```


가 된다.

> 표현이 두 가지인 수는 1을 쓰지 않는 쪽을 택하면 된다. 예를 들어 `\(\tfrac13 = 0.1000\cdots_{(3)} = 0.0222\cdots_{(3)}\)`이므로 `\(\tfrac13 \in C\)`다. 끝점이 살아남는다는 것과 같은 이야기다.

이제 `\(C\)`의 크기가 보인다. 각 자리에서 0이냐 2냐를 자유롭게 고르므로 `\(C\)`는 `\(\{0,2\}^{\mathbb{N}}\)`과 일대일 대응한다. 즉 `\(C\)`는 **비가산집합**이다.

이제 그 위에 분포를 얹는다. 이것도 push-forward로 만들어진다.

공정한 동전을 무한히 던지는 확률공간


```math
\Omega = \{0,1\}^{\mathbb{N}},
\qquad
\omega = (b_1, b_2, b_3, \ldots),b_n \in \{0,1\}
\qquad
b_n \overset{iid}{\sim} \operatorname{Bernoulli}(\tfrac12)
```


에서 시작해, 함수 `\(X : \Omega \to [0,1]\)`을


```math
X(\omega) = \sum_{n=1}^{\infty} \frac{2 b_n}{3^{n}}
```


로 정의하자.

이 함수가 하는 일은 이렇다. `\(b_n \in \{0,1\}\)`이므로 `\(2 b_n \in \{0,2\}\)`다. 즉 `\(X(\omega)\)`의 **`\(n\)`번째 3진 자리를 `\(n\)`번째 동전이 정한다.**


```math
b_n = 0 \ \mapsto\ d_n = 0,
\qquad
b_n = 1 \ \mapsto\ d_n = 2
```


숫자 1은 절대 나오지 않는다. 그래서 `\(X(\omega)\)`는 언제나 `\(C\)`의 원소다.

몇 개 넣어보면 감이 온다.

| `\(\omega\)` | 3진 전개 | `\(X(\omega)\)` |
| --- | --- | --- |
| `\((0,0,0,\ldots)\)` | `\(0.000\cdots_{(3)}\)` | `\(0\)` |
| `\((1,1,1,\ldots)\)` | `\(0.222\cdots_{(3)}\)` | `\(1\)` |
| `\((1,0,0,0,\ldots)\)` | `\(0.200\cdots_{(3)}\)` | `\(\tfrac23\)` |
| `\((0,1,0,1,\ldots)\)` | `\(0.0202\cdots_{(3)}\)` | `\(\tfrac14\)` |

기하적으로 읽으면 더 직관적이다. `\(n\)`단계에는 `\(2^{n}\)`개의 구간이 남아 있는데, 그중 어디로 갈지를 매 단계 동전으로 고르는 것이다. `\(b_n = 0\)`이면 왼쪽 조각, `\(b_n = 1\)`이면 오른쪽 조각. 무한히 고르고 나면 구간이 한 점으로 좁혀지고, 그 점이 `\(X(\omega)\)`다.

두 가지만 확인해두자.

- **잘 정의된다.** `\(\sum_{n} 2 \cdot 3^{-n} = 1\)`이므로 급수는 항상 수렴하고 `\(X(\omega) \in [0,1]\)`이다.
- **가측이다.** 부분합 `\(X_N(\omega) = \sum_{n \le N} 2 b_n 3^{-n}\)`은 유한개의 좌표만 보므로 가측이고, `\(X\)`는 그 점별극한이다. 4절에서 본 성질이 그대로 쓰인다.

이때 `\(P_X = X_{\#}P\)`를 **Cantor 분포**라고 한다.

그러면 앞의 두 식이 곧바로 나온다.

- `\(X\)`가 만드는 수는 3진 자리가 전부 0 또는 2이므로 **항상** `\(C\)` 안에 떨어진다. 즉 `\(X^{-1}(C) = \Omega\)`이고 `\(P_X(C) = 1\)`이다.
- 특정 `\(x \in C\)`를 찍으면 그에 대응하는 동전 수열이 하나로 정해진다. `\(X = x\)`가 되려면 무한히 많은 동전이 **전부** 그대로 나와야 하므로 `\(P_X(\{x\}) = \lim_{n} 2^{-n} = 0\)`이다.

> **모순처럼 보이지만 아니다.** 확률의 가산가법성은 **가산개** 집합에만 적용된다. `\(C\)`는 비가산이므로 `\(P_X(C) = \sum_{x \in C} P_X(\{x\})\)`라고 쓸 수 없다. 사실 10절의 `\(\operatorname{Unif}[0,1]\)`에서 이미 같은 일을 겪었다. 모든 점의 확률이 0인데 구간 전체는 1이었다.

---

# 막간: push-forward로 보는 ML 네 가지

지금까지 만든 push-forward는 여기서부터 네 절 동안 실제로 쓰인다.

**14절부터 17절까지**는 잠시 이론을 멈추고, 이 도구가 머신러닝에서 어떻게 쓰이는지를 본다. 역변환 샘플링, reparameterization trick, normalizing flow, GAN 네 가지다. 겉보기에는 서로 다른 기법이지만 넷 다 같은 문장을 쓰고 있다.


```math
\boxed{
\text{다루기 쉬운 분포}
\overset{\text{가측함수}}{\longrightarrow}
\text{원하는 분포}
}
```


다른 것은 어떤 함수를 쓰느냐뿐이다. 그리고 그 선택이 어디까지 데려가는지는 마지막 열이 보여준다.

| 절 | 기법 | 출발 분포 | 함수 | 도착 분포 | 밀도 |
| --- | --- | --- | --- | --- | --- |
| 14 | 역변환 샘플링 | `\(\operatorname{Unif}(0,1)\)` | `\(F^{-1}\)` | CDF가 `\(F\)`인 분포 | `\(F\)`에 따라 |
| 15 | Reparameterization trick | `\(N(0,1)\)` | `\(\varepsilon \mapsto \mu + \sigma\varepsilon\)` | `\(N(\mu, \sigma^2)\)` | 있음 |
| 16 | Normalizing flow | 간단한 base `\(p_0\)` | 가역함수의 합성 `\(f_K \circ \cdots \circ f_1\)` | 복잡한 `\(P_{Z_K}\)` | 있음 |
| 17 | GAN | `\(N(0, I_d)\)` | 생성자 `\(G\)` (`\(d \ll D\)`, 비가역) | `\(P_g\)` | **없음** |

앞의 셋은 밀도를 가진 분포로 끝나지만 GAN은 그렇지 않다. 13절에서 본 밀도 없는 분포가 거기서 다시 나온다.

**18절로 건너뛰어도 이후 전개에는 지장이 없다.**

---

# 14. 역변환 샘플링이 왜 되는가

CDF와 push-forward를 알고 나면 역변환 샘플링도 자연스럽게 보인다.

만들고 싶은 분포의 CDF를 `\(F\)`라고 하자. 먼저


```math
U \sim \operatorname{Unif}(0, 1)
```


을 뽑고


```math
X = F^{-1}(U)
```


라고 하자.

> `\(U \sim \operatorname{Unif}(0,1)\)`이라는 표기가 확률공간 `\((\Omega, \mathcal{F}, P)\)`의 언어로 정확히 무엇을 주장하는지는 이 절 끝의 추가 설명에서 다룬다. 지금 필요한 것은 `\(P(U \le t) = t\)` 하나뿐이다.

그러면


```math
\begin{aligned}
P(X \le x)
&= P(F^{-1}(U) \le x) \\
&= P(U \le F(x)) \\
&= F(x).
\end{aligned}
```


따라서 `\(X\)`의 CDF가 `\(F\)`다.

즉


```math
\boxed{
U \sim \operatorname{Unif}(0, 1)
\overset{F^{-1}}{\longmapsto}
X, \qquad F_X = F
}
```


이다.

측도 관점에서는


```math
\boxed{
P_X = (F^{-1})_{\#}\operatorname{Unif}(0, 1)
}
```


이라고 말할 수 있다.

일반적인 CDF가 엄격히 증가(strictly increasing)하지 않을 수도 있으므로 엄밀하게는 generalized inverse


```math
F^{-1}(u) = \inf\{x : F(x) \ge u\}
```


를 사용한다. 엄격히 증가하지 않으면 역함수 `\(F^{-1}\)`가 존재하지 않기 때문이다.

즉 역변환 샘플링은 어떤 별개의 샘플링 기술이라기보다


```math
\boxed{\text{균등분포를 원하는 분포로 push-forward하는 방법}}
```


이다.

## `\(U \sim \operatorname{Unif}(0, 1)\)`은 확률공간에서 무슨 뜻인가

> 위 계산에서 실제로 쓴 것은 `\(P(U \le F(x)) = F(x)\)` 한 줄뿐이다. 그 표기가 확률공간의 언어로 정확히 무엇을 주장하는지, 그리고 `\(\Omega\)`를 한 번도 밝히지 않고 넘어갈 수 있는 이유가 궁금하지 않다면 건너뛰어도 좋다.

### `\(\sim\)`는 함수가 아니라 push-forward에 대한 진술이다

`\(U \sim \operatorname{Unif}(0,1)\)`은 `\(U\)`라는 **함수**가 어떻게 생겼는지를 말하지 않는다. 9절의 언어로 옮기면 이 표기는 측도들 사이의 등식 하나다.


```math
\boxed{
U \sim \operatorname{Unif}(0, 1)
\iff
P_U = U_{\#}P = \operatorname{Unif}(0, 1)
}
```


풀어 쓰면 **모든** Borel 집합 `\(B \in \mathcal{B}(\mathbb{R})\)`에 대해


```math
P\big(U^{-1}(B)\big) = \operatorname{Leb}\big(B \cap (0,1)\big)
```


이다. 즉 `\(\operatorname{Unif}(0,1)\)`은 어떤 함수의 이름이 아니라 실수축 위의 **확률측도 하나**의 이름이고, `\(\sim\)`는 “`\(U\)`의 분포가 그 측도와 같다”는 등식이다.

같은 말을 쓰는 표기가 몇 가지 있다.


```math
U_{\#}P = \operatorname{Unif}(0,1),
\qquad
P \circ U^{-1} = \operatorname{Unif}(0,1),
\qquad
\mathcal{L}(U) = \operatorname{Unif}(0,1)
```


9절의 도식에 얹으면


```math
(\Omega, \mathcal{F}, P)
\overset{U}{\longrightarrow}
\big(\mathbb{R}, \mathcal{B}(\mathbb{R}), \operatorname{Unif}(0,1)\big).
```


### 그러면 `\(\Omega\)`는 무엇인가

두 가지로 읽으면 된다.

**존재 선언으로 읽기.** 보통은 이 뜻이다.

> 어떤 확률공간 `\((\Omega, \mathcal{F}, P)\)`와 가측함수 `\(U : \Omega \to \mathbb{R}\)`가 존재해서 `\(U_{\#}P = \operatorname{Unif}(0,1)\)`이다.

`\(\Omega\)`를 정하지 않은 것이 아니라, 뒤따르는 계산이 `\(\Omega\)`에 의존하지 않으므로 **말할 필요가 없어서 말하지 않는 것**이다.

**표준 실현으로 읽기.** 굳이 하나 지목해야 한다면 구간 자체를 표본공간으로 잡으면 된다.


```math
\boxed{
(\Omega, \mathcal{F}, P) = \big((0,1),\ \mathcal{B}((0,1)),\ \operatorname{Leb}\big),
\qquad
U(\omega) = \omega
}
```


즉 **항등함수**다. 그러면


```math
P_U(B) = P(\{\omega \in (0,1) : \omega \in B\}) = \operatorname{Leb}(B \cap (0,1))
```


이므로 곧바로 `\(U \sim \operatorname{Unif}(0,1)\)`이다. 균등확률변수의 존재를 따로 증명할 필요가 없는 이유가 이것이다. `\((0,1)\)`에 제한한 Lebesgue 측도가 이미 확률측도이고, 균등확률변수는 그 위의 항등사상이다.

### 왜 `\(\Omega\)`를 밝히지 않아도 되는가

8절의 결론이 그대로 근거가 된다. 우리가 쓰는 양은 전부 `\(P_U\)`만 거쳐서 계산된다.


```math
P(U \le t) = P_U((-\infty, t]),
\qquad
\mathbb{E}[g(U)] = \int_{\Omega} g(U(\omega))\,dP(\omega) = \int_{\mathbb{R}} g(u)\,dP_U(u)
```


오른쪽 어디에도 `\(\Omega\)`가 남아 있지 않다. 그래서 `\(\sim\)`는 사실상 **분포가 같은 확률변수들을 한 덩어리로 묶고 그 덩어리의 이름을 부르는 표기**다. 12절에서 본 이야기와 같다. 분포가 같다고 확률변수가 같은 것은 아니다.

실제로 `\(\operatorname{Unif}(0,1)\)`을 주는 확률변수는 하나가 아니다.

| `\((\Omega, \mathcal{F}, P)\)`                                                                   | `\(U(\omega)\)`                                          |                 |
| -------------------------------------------------------------------------------------------- | ---------------------------------------------------- | --------------- |
| `\(\big((0,1),\ \mathcal{B},\ \operatorname{Leb}\big)\)`                                         | `\(\omega\)`                                             | 표준 실현           |
| `\(\big((0,1),\ \mathcal{B},\ \operatorname{Leb}\big)\)`                                         | `\(1 - \omega\)`                                         | 함수는 다르지만 법칙은 같다 |
| `\(\Omega = \{0,1\}^{\mathbb{N}},\ b_n \overset{iid}{\sim} \operatorname{Bernoulli}(\tfrac12)\)` | `\(\displaystyle\sum_{n=1}^{\infty} \frac{b_n}{2^{n}}\)` | 동전 무한수열의 2진 전개  |

---

# 15. Reparameterization trick도 똑같은 그림이다

VAE에서 자주 보는


```math
z = \mu + \sigma\varepsilon, \qquad \varepsilon \sim N(0, 1)
```


을 생각해보자.

함수


```math
T_{\mu, \sigma}(\varepsilon) = \mu + \sigma\varepsilon
```


를 정의하면


```math
z = T_{\mu, \sigma}(\varepsilon).
```


그리고


```math
\varepsilon \sim N(0, 1)
```


이므로


```math
\boxed{
P_z = (T_{\mu, \sigma})_{\#}N(0, 1)
}
```


이다.

결과적으로


```math
z \sim N(\mu, \sigma^2).
```


즉 reparameterization은


```math
\boxed{
\text{단순한 고정 noise distribution}
\overset{T_{\mu, \sigma}}{\longrightarrow}
\text{원하는 parameterized distribution}
}
```


이라는 push-forward다.

reparameterization trick의 핵심은 랜덤성을


```math
z \sim N(\mu, \sigma^2)
```


에서 직접 발생시키는 대신


```math
\varepsilon \sim N(0, 1)
```


라는 파라미터와 무관한 noise에 모아놓고


```math
z = T_{\mu, \sigma}(\varepsilon)
```


라는 미분 가능한 함수로 표현한다는 데 있다.

그래서 gradient를


```math
\mu, \sigma
```


를 지나서 역전파할 수 있다.

---

# 16. Normalizing flow도 push-forward다

Normalizing flow에서는 간단한 base distribution


```math
Z_0 \sim p_0
```


에서 시작한다.

그리고 가역함수


```math
f_1, f_2, \dots, f_K
```


를 차례로 적용한다.


```math
Z_K = f_K \circ \cdots \circ f_1(Z_0).
```


그러면 최종 분포는


```math
\boxed{
P_{Z_K} = (f_K \circ \cdots \circ f_1)_{\#}P_{Z_0}
}
```


이다.

즉 normalizing flow 역시 본질적으로


```math
\boxed{\text{간단한 측도를 함수로 밀어 복잡한 측도를 만드는 모델}}
```


이다.

다만 flow에서는 함수가 가역이기 때문에 확률밀도가 어떻게 늘어나고 줄어드는지도 추적할 수 있다.

그 결과 change-of-variables formula


```math
p_Y(y) = p_X(f^{-1}(y)) \left| \det Df^{-1}(y) \right|
```


가 등장한다.

push-forward가 **분포가 어떻게 이동하는가**를 말한다면 Jacobian determinant는 그 과정에서 **밀도가 어떻게 변하는가**를 추적한다.

---

# 17. GAN은 밀도가 없는 push-forward다

앞의 세 가지는 모두 밀도를 가진 분포로 끝났다. 같은 push-forward인데 결과가 전혀 다른 경우를 하나 보자.

GAN의 생성자는


```math
G : \mathbb{R}^{d} \longrightarrow \mathbb{R}^{D},
\qquad
d \ll D
```


이다. 저차원 latent


```math
z \sim P_z = N(0, I_d)
```


를 받아 고차원 데이터 공간의 점 `\(G(z)\)`를 내놓는다. 모델이 만드는 분포는 지금까지와 똑같이 push-forward다.


```math
\boxed{
P_g = G_{\#}P_z
}
```


여기까지는 15절, 16절과 다를 것이 없다. 문제는 **목적지의 차원이 출발지보다 훨씬 크다**는 데서 생긴다.

`\(G\)`가 립시츠 연속이면 상 `\(G(\mathbb{R}^{d})\)`는 `\(\mathbb{R}^{D}\)` 안에서 기껏해야 `\(d\)`차원짜리 집합이다. `\(d \ll D\)`이므로 이 집합은 `\(D\)`차원 부피를 갖지 않는다.


```math
\operatorname{Leb}_{D}\big(G(\mathbb{R}^{d})\big) = 0
```


> **왜 연속이 아니라 립시츠인가.** 연속만으로는 부족하다. 페아노 곡선처럼 `\([0,1]\)`을 정사각형 `\([0,1]^2\)` 전체로 덮어버리는 연속함수가 실제로 존재하기 때문이다. 반면 립시츠 사상은 거리를 상수배 이상으로 늘리지 못해 집합의 차원을 키울 수 없고, 그래서 `\(d < D\)`이면 상의 `\(D\)`차원 부피가 0이 된다. ReLU나 tanh를 쓰는 보통의 신경망은 유계 영역에서 립시츠이므로 이 조건이 실제로 걸림돌이 되지는 않는다.

그런데 `\(P_g\)`는 이 집합에 확률을 전부 몰아준다. `\(z\)`가 무엇이든 `\(G(z)\)`는 반드시 이 안에 떨어지기 때문이다.


```math
P_g\big(G(\mathbb{R}^{d})\big) = 1
```


즉 **부피가 0인 집합 위에 확률 1이 놓여 있다.** 13절에서 이미 본 상황이다. 그때는 길이가 0인 Cantor 집합 `\(C\)` 위에 확률 1이 놓였다. 차원만 올라갔을 뿐 구조가 같다.

따라서 `\(P_g\)`에는 Lebesgue 밀도가 없다. 밀도 `\(p_g\)`가 있다고 가정하면


```math
1 = P_g\big(G(\mathbb{R}^{d})\big) = \int_{G(\mathbb{R}^{d})} p_g(x)\,dx = 0
```


이 되어 모순이다. 13절에서 Cantor 분포에 밀도가 없음을 보인 논증과 글자 하나 다르지 않다.


```math
\boxed{
\text{GAN이 만드는 } P_g \text{ 에는 밀도 } p_g(x) \text{ 가 존재하지 않는다}
}
```


13절에서 예고한

> GAN에서 우도(likelihood)를 직접 쓰지 못하는 이유가 이것이다.

의 정체가 이것이다. 보통의 생성모델은 로그우도


```math
\max_{\theta} \ \frac{1}{n}\sum_{i=1}^{n} \log p_{\theta}(x_i)
```


를 올려서 학습한다. 그런데 `\(p_{\theta}\)` 자체가 존재하지 않으면 이 식은 쓸 수가 없다. 적어낼 수 없는 것을 최대화할 수는 없다.

밀도를 비교하는 다른 척도들도 같은 벽에 부딪힌다. (KL이나 Jensen-Shannon divergence)

그래서 GAN은 밀도를 포기하고 **표본만으로 두 분포를 비교하는** 길을 택한다. 판별자 `\(D\)`가 그 역할을 한다. 판별자는 진짜 표본과 `\(G(z)\)`를 구별하려 하고, 생성자는 구별하지 못하게 만들려 한다. 밀도를 사용하지 않고 분포를 맞춰가는 방식이다.

> 밀도 비율 대신 **공간 위의 거리**로 두 분포를 비교하면 이 벽을 피할 수 있다. Wasserstein 거리가 그것이고 WGAN이 거기서 나온다.

16절과 나란히 놓으면 normalizing flow가 굳이 **가역**함수만 쓰는 이유가 분명해진다.

|  | Normalizing flow (16절) | GAN (17절) |
| --- | --- | --- |
| 함수 | 가역, 차원 보존 `\(\mathbb{R}^{D} \to \mathbb{R}^{D}\)` | 비가역, 차원 확대 `\(\mathbb{R}^{d} \to \mathbb{R}^{D}\)` |
| push-forward한 분포 | 밀도 있음 | 밀도 없음 |
| 밀도 추적 | Jacobian determinant로 가능 | 불가능 |
| 학습 신호 | 로그우도 직접 최대화 | 판별자를 통한 적대적 학습 |
| 대가 | 구조가 차원에 묶인다 | 우도를 잃는다 |

> **manifold hypothesis.** 실제 데이터가 고차원 공간 안의 저차원 manifold 위에 놓여 있다는 가설이다. 이것이 맞다면 `\(P_{\text{data}}\)` 자체에도 밀도가 없다. 그렇다면 밀도 없는 분포를 만드는 것은 GAN의 결함이 아니라 오히려 데이터를 닮은 것이 된다. 21절에서 push-forward의 목적지를 manifold로 옮기는 이야기와 이어진다.

---

# ML 응용 한 줄 요약

네 절을 한 식으로 남긴다면


```math
\boxed{
\text{간단한 확률공간} + \text{가측함수}
\longrightarrow \text{새로운 확률분포}
}
```


이다. 바뀌는 것은 가운데 함수 하나뿐이다.

| 기법 | ML에서 쓰는 문장 | push-forward로 읽으면 |
| --- | --- | --- |
| 역변환 샘플링 (14절) | `\(U \sim \operatorname{Unif}(0,1),\; X = F^{-1}(U)\)` | `\(P_X = (F^{-1})_{\#}\operatorname{Unif}(0,1)\)` |
| Reparameterization trick (15절) | `\(\varepsilon \sim N(0,1),\; z = \mu + \sigma\varepsilon\)` | `\(P_z = (T_{\mu, \sigma})_{\#}N(0,1)\)` |
| Normalizing flow (16절) | `\(Z_0 \sim p_0,\; Z_K = f_K \circ \cdots \circ f_1(Z_0)\)` | `\(P_{Z_K} = (f_K \circ \cdots \circ f_1)_{\#}P_{Z_0}\)` |
| GAN (17절) | `\(z \sim P_z = N(0, I_d),\; x = G(z)\)` | `\(P_g = G_{\#}P_z\)` |

왼쪽 열은 ML에서 보는 표기이고, 오른쪽 열은 그 표기가 실제로 말하는 **측도들 사이의 등식**이다. 네 기법의 차이는 어떤 가측함수를 고르느냐뿐이고, GAN만 `\(d \ll D\)` 때문에 도착한 분포에 밀도가 없다.

---

# 18. `\(\sigma(X)\)`: 확률변수가 알려주는 정보

앞에서 σ-대수를


```math
\boxed{\text{현재 정보로 구별 가능한 사건들의 모음}}
```


이라고 해석했다.

그러면 확률변수 `\(X\)`를 관측했을 때 얻는 정보도 σ-대수로 표현할 수 있을까?

가능하다.


```math
\boxed{
\sigma(X) = \{X^{-1}(B) : B \in \mathcal{B}(\mathbb{R})\}
}
```


를 `\(X\)`가 생성하는 σ-대수라고 한다.

조금 더 직관적으로는


```math
\boxed{
\sigma(X) = X\text{의 값만 보고 판별할 수 있는 모든 사건}
}
```


이다.

---

# 19. 다시 동전 두 번 던지기


```math
\Omega = \{HH, HT, TH, TT\}
```


이고 `\(X\)`를 앞면의 개수라고 하자.


```math
X(HH) = 2, \qquad X(HT) = X(TH) = 1, \qquad X(TT) = 0.
```


`\(X\)`를 관측하면 세 경우를 구별할 수 있다.


```math
\{HH\}, \qquad \{HT, TH\}, \qquad \{TT\}.
```


하지만


```math
\{HT\}
```


라는 사건은 `\(X\)`만 보고는 알 수 없다.

왜냐하면


```math
X(HT) = X(TH) = 1
```


이기 때문이다.

따라서


```math
\{HT\} \notin \sigma(X).
```


반면

> “앞면이 정확히 한 개다.”

라는 사건은


```math
\{HT, TH\} = X^{-1}(\{1\})
```


이므로


```math
\{HT, TH\} \in \sigma(X).
```


즉


```math
\boxed{
X \text{가 같은 값을 주는 결과들은 } X \text{만 보고 구별할 수 없다.}
}
```


---

# 20. 이것이 조건부기댓값으로 이어진다

나중에


```math
E[Y \mid X]
```


라는 것을 배우게 된다.

처음 보면

> “`\(X\)`가 주어졌을 때 `\(Y\)`의 평균”

이라고 배우지만 측도론적으로 정확한 표현은


```math
\boxed{
E[Y \mid X] = E[Y \mid \sigma(X)]
}
```


이다.

즉

> **`\(X\)`를 관측해서 얻을 수 있는 정보만 사용했을 때 `\(Y\)`를 가장 잘 설명하는 것**

이다.

그래서 이번 장의


```math
\sigma(X)
```


가 뒤에서 조건부기댓값과 filtration을 이해하는 핵심 재료가 된다.

---

# 21. Push-forward의 목적지는 `\(\mathbb{R}^n\)`일 필요가 없다

> 본편은 20절에서 끝난다. 이 절은 push-forward의 목적지를 `\(S^2\)`나 `\(SO(3)\)` 같은 manifold로 넓히는 확장이다. 궁금하지 않다면 바로 마무리로 넘어가도 좋다.

여기까지는


```math
X : \Omega \to \mathbb{R}
```


또는


```math
X : \Omega \to \mathbb{R}^n
```


만 생각했다.

하지만 가측함수의 목적지는 꼭 Euclidean space일 필요가 없다.

측정공간


```math
(M, \mathcal{B}(M))
```


만 정의되어 있다면


```math
T : \Omega \to M
```


로 측도를 밀어낼 수 있다.

여기서 `\(M\)`은 표본공간이 아니라 **도착공간**이다. 출발지는 여전히 확률공간 `\((\Omega, \mathcal{F}, P)\)`이고, 1절에서 `\((S, \mathcal{S})\)`라고 쓴 자리에 `\(M\)`이 들어간 것뿐이다. 그리고 `\(\mathcal{B}(M)\)`은 `\(M\)`의 열린집합들이 생성하는 Borel σ-대수다.

이렇게 `\(\mathbb{R}\)`이 아닌 공간에 값을 갖는 가측함수는 확률변수가 아니라 **확률원소**(random element)라고 부른다. 확률변수는 `\(S = \mathbb{R}\)`인 특수한 경우다.

예를 들어


```math
Z \sim N(0, I_3)
```


라고 하자. 여기서 `\(I_3\)`는 `\(3 \times 3\)` 단위행렬이고 공분산행렬 자리에 온다. 즉 `\(Z\)`는 `\(\mathbb{R}^3\)`에 값을 갖는 확률변수이고, 세 좌표가 각각 독립인 표준정규라는 뜻이다.


```math
Z = (Z_1, Z_2, Z_3), \qquad Z_1, Z_2, Z_3 \overset{\text{iid}}{\sim} N(0, 1)
```


`\(\sim\)`는 `\(Z\)`라는 **함수**가 어떻게 생겼는지를 말하지 않는다. 이 표기가 약속하는 것은 측도들 사이의 등식 `\(P_Z = Z_{\#}P = N(0, I_3)\)` 하나뿐이다. 자세한 것은 14절의 추가 설명에 있다.

여기에


```math
T(z) = \frac{z}{\|z\|}
```


를 적용한다.

> **대문자와 소문자.** 대문자 `\(Z\)`는 확률변수, 즉 `\(\Omega\)` 위에 정의된 함수 `\(Z : \Omega \to \mathbb{R}^3\)`이다. 반면 `\(T(z) = z / \|z\|\)`의 소문자 `\(z\)`는 `\(\mathbb{R}^3\)`의 한 점이다. 그래서 아래에서 쓰는 `\(Z / \|Z\|\)`는 두 함수의 합성 `\(T \circ Z : \Omega \xrightarrow{\;Z\;} \mathbb{R}^3 \xrightarrow{\;T\;} S^2\)`를 뜻한다. 17절에서 GAN의 latent를 소문자 `\(z\)`로 쓴 것은 ML 논문의 관례를 따른 것이다.

`\(N(0, I_3)\)`의 밀도는


```math
p(z) = \frac{1}{(2\pi)^{3/2}} \exp\left(-\frac{\|z\|^2}{2}\right)
```


로, `\(z\)`에 오직 `\(\|z\|\)`를 통해서만 의존한다. 따라서 임의의 직교변환 `\(R \in O(3)\)`(회전과 반사)에 대해 `\(\|Rz\| = \|z\|\)`이므로 밀도가 변하지 않는다. push-forward의 언어로 쓰면


```math
\boxed{
R_{\#}P_Z = P_Z \qquad (\forall R \in O(3))
}
```


이고, 이것이 **`\(N(0, I_3)\)`는 회전대칭**이라는 말의 뜻이다.

이제 `\(T\)`를 통과시킨다. 먼저 `\(T\)`가 회전과 교환된다는 것을 확인하자. `\(R\)`은 길이를 보존하고 선형이므로


```math
T(Rz) = \frac{Rz}{\|Rz\|} = \frac{Rz}{\|z\|} = R\left(\frac{z}{\|z\|}\right) = R\,T(z)
```


이다. 먼저 돌리고 정규화하나, 정규화하고 돌리나 같다는 뜻이다.

이 성질과 회전대칭을 합치면 `\(Z / \|Z\|\)`의 분포가 회전불변임이 나온다. 구면 위의 집합 `\(B \subseteq S^2\)`에 대해 `\(\nu(B) = P(Z / \|Z\| \in B)\)`라고 두고, `\(B\)`를 회전시킨 `\(RB\)`에서 계산해보자.


```math
\nu(RB)
= P\left(\frac{Z}{\|Z\|} \in RB\right)
= P\left(R^{-1}\frac{Z}{\|Z\|} \in B\right)
= P\left(\frac{R^{-1}Z}{\|R^{-1}Z\|} \in B\right)
= P\left(\frac{Z}{\|Z\|} \in B\right)
= \nu(B)
```


두 번째 등호는 `\(R\)`이 전단사이기 때문이고, 세 번째 등호가 `\(T\)`의 교환성이고, 네 번째 등호가 가우시안의 회전대칭 `\(R_{\#}P_Z = P_Z\)`다.

여기서 교환성이 하는 일이 핵심이다. 회전대칭은 `\(\mathbb{R}^3\)` 위의 가우시안이 가진 성질인데, 우리가 알고 싶은 것은 구면 위 분포의 성질이다. 교환성은 **구면에서 하던 회전을 `\(\mathbb{R}^3\)` 안으로 옮겨주는 다리**여서, 옮겨간 자리에서 가우시안의 대칭성을 쓸 수 있게 해준다.

> **두 성질이 모두 필요하다.** `\(Z \sim N(0, \operatorname{diag}(1, 1, 4))\)`처럼 회전대칭이 아닌 가우시안을 쓰면 `\(T\)`의 교환성은 그대로지만 네 번째 등호가 깨진다. 실제로 이때 `\(Z / \|Z\|\)`는 극 방향에 몰리고 균등분포가 아니다.

> push-forward로 쓰면 같은 계산이 한 줄이다. `\(R_{\#}(T_{\#}P_Z) = (R \circ T)_{\#}P_Z = (T \circ R)_{\#}P_Z = T_{\#}(R_{\#}P_Z) = T_{\#}P_Z\)`. 여기서 쓴 합성 규칙 `\((g \circ f)_{\#}\mu = g_{\#}(f_{\#}\mu)\)`는 `\((g \circ f)^{-1}(B) = f^{-1}(g^{-1}(B))\)`에서 바로 나온다.

그런데 구면 위에서 회전불변인 확률측도는 균등분포 하나뿐이다. 그래서


```math
\frac{Z}{\|Z\|}
```


는 구면


```math
S^2 = \{x \in \mathbb{R}^3 : \|x\| = 1\}
```


위의 균등분포를 따른다.

> `\(T(z) = z / \|z\|\)`는 `\(z = 0\)`에서 정의되지 않는다. 하지만 `\(P(Z \neq 0) = 1\)`, 즉 **`\(Z\)`가 `\(T\)`의 정의역에 떨어진다는 사건이 확률 1**이므로 `\(Z / \|Z\|\)`는 확률 1인 사건 위에서 정의된다. 남은 크기가 0인 집합 위에서 값을 어떻게 주든 push-forward된 분포는 달라지지 않는다.

즉


```math
\boxed{
N(0, I_3)
\overset{z / \|z\|}{\longrightarrow}
\operatorname{Unif}(S^2)
}
```


이다.

이번에는


```math
Q \sim N(0, I_4)
```


를 정규화해


```math
\hat{Q} = \frac{Q}{\|Q\|} \in S^3
```


로 만들고 이를 unit quaternion으로 해석해 회전행렬


```math
R(\hat{Q}) \in SO(3)
```


로 보내자.

그러면


```math
\boxed{
N(0, I_4) \longrightarrow S^3 \longrightarrow SO(3)
}
```


라는 push-forward를 통해 `\(SO(3)\)` 위의 균등한 회전분포, 즉 Haar uniform distribution을 만들 수 있다.


---

# 마무리

확률공간


```math
(\Omega, \mathcal{F}, P)
```


에서 시작한다.

가측함수


```math
X : \Omega \to \mathbb{R}
```


를 하나 선택한다.

그러면 세 가지가 동시에 생긴다.

첫째, 실제 결과를 숫자로 바꾼다.


```math
\omega \mapsto X(\omega).
```


둘째, `\(X\)`로 알아낼 수 있는 정보를 만든다.


```math
\mathcal{F} \supseteq \sigma(X).
```


셋째, 원래 확률측도를 실수축으로 밀어내 분포를 만든다.


```math
P \overset{X}{\longmapsto} P_X = X_{\#}P.
```


따라서


```math
\boxed{
\begin{array}{ccc}
(\Omega, \mathcal{F}, P)
& \xrightarrow{\quad X \quad} &
(\mathbb{R}, \mathcal{B}(\mathbb{R}), P_X) \\[2mm]
\text{원래 세계} & & \text{관측된 값의 세계}
\end{array}
}
```


라고 생각할 수 있다.

여기서


```math
\boxed{
P_X(B) = P(X^{-1}(B))
}
```


라는 단 하나의 식이 거의 모든 것을 연결한다.

이 식 하나에

- 왜 확률변수가 가측함수여야 하는지
- 확률변수의 분포가 무엇인지
- push-forward가 무엇인지
- CDF가 어떻게 만들어지는지

가 모두 들어 있다.

그리고 정보의 관점에서는 또 하나의 식을 기억하면 된다.


```math
\boxed{
\sigma(X) = \{X^{-1}(B) : B \in \mathcal{B}(\mathbb{R})\}
}
```


즉


```math
\boxed{
\text{확률변수 } X =
\begin{cases}
\text{결과를 값으로 바꾸는 함수} \\
\text{확률측도를 새로운 공간으로 밀어내는 함수} \\
\text{우리가 관측할 수 있는 정보를 결정하는 함수}
\end{cases}
}
```


이다.
