---
title: "Measure Theory for AI"
layout: "series"
description: "해석학을 따로 배운 적 없는 AI 전공자를 위한 측도론 강의 노트. σ-대수에서 시작해 확률 커널과 SDE까지 간다."
ShowToc: false
summary: "σ-대수부터 확률 커널과 SDE까지, ML 논문의 측도론적 언어를 읽기 위한 강의 노트 시리즈."
upcoming_title: "앞으로 올라올 강"
upcoming:
  - "**4강 — 르베그 적분과 수렴정리** · 극한과 적분은 언제 교환되는가 (MCT, Fatou, DCT)"
  - "**5강 — 기댓값, Lᵖ 공간, 부등식** · LOTUS, Jensen·Hölder·Markov, L² 사영"
  - "**6강 — 곱측도, Fubini, 독립성** · iid의 정확한 의미"
  - "**7강 — Radon–Nikodym과 밀도** · 밀도는 언제 존재하는가, KL과 importance sampling"
  - "**8강 — 조건부 기댓값** · 확률 0인 사건에 조건화하기, 회귀 = L² 사영"
  - "**9강 — 확률 커널과 측도론적 베이즈 정리** · disintegration"
  - "**10강 — 확률과정, 마르코프 연쇄, 마팅게일** · 필트레이션과 전이 커널"
  - "**11강 — 브라운 운동과 SDE** · diffusion 모델의 수학 (Itô 공식, Fokker–Planck)"
---

> - **대상** — 해석학 배경이 없다고 가정한 AI 전공 대학원생
> - **목표** — ML 논문에 나오는 측도론적 언어(σ-대수, 밀도, KL, 조건부 기댓값, 확률 커널, SDE)를 읽고 쓸 수 있게 되는 것
> - **원칙** — 증명보다 동기와 반례. 매 강은 “ML에서 이게 없으면 깨지는 지점”에서 출발하고, 정리는 API처럼 다룬다 (가설·결론·깨지는 조건만 정확히)

번호는 커리큘럼상의 강 번호다. 1강(왜 측도론인가)에서 다루려던 것 — 모든 부분집합에 길이를 줄 수는 없다는 사실, Vitali 집합 — 은 2강 글의 0절과 8절이 그대로 흡수했으므로, 읽는 순서는 **2강부터**다.

주교재는 Rosenthal, *A First Look at Rigorous Probability Theory*. 참고로 Axler, *Measure, Integration & Real Analysis*와 Tao, *An Introduction to Measure Theory* (둘 다 무료 공개)를 함께 쓴다.
