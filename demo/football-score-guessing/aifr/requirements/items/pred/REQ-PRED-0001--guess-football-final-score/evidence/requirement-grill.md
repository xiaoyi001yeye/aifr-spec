# Requirement Grill Evidence

Requirement id: REQ-PRED-0001

## Conversation Decisions

1. Data source
   - Question: 娱乐随机生成，还是基于真实球队、赛程、历史数据预测？
   - Answer: 娱乐性质的猜比分，不依赖外部数据。

2. Randomness
   - Question: 同样两个球队返回固定比分，还是每次可以随机变化？
   - Answer: 随机比分就行。

3. Score range
   - Question: 比分范围是否限制在足球常见范围，还是允许夸张娱乐比分？
   - Answer: 让比分更像真实的比分，也不排除大比分的结果，但是不能非常离谱。

4. Team ordering
   - Question: 是否区分主队/客队，还是按输入顺序展示？
   - Answer: 同意按输入顺序展示，不区分主客场。

5. Invalid input
   - Question: 空队名、只输入一个队、两个队名相同是否拒绝生成？
   - Answer: 同意。

6. Disclaimer
   - Question: 是否必须包含“仅供娱乐，不保证准确”的免责声明？
   - Answer: 同意。

7. Interaction surface
   - Question: demo 描述网页表单、API 接口，还是命令行输入？
   - Answer: 有个简单的网页吧。

## Working Interpretation

- The product is a simple web page.
- The generator does not fetch or infer real football data.
- Goal counts should be bounded at 0-7.
- A weighted random strategy should make 0-3 more common than 4-7.
- Results are shown as `team_a goals : team_b goals` in input order.

