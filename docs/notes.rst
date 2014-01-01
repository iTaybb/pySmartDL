Notes
===================================

========================
Bytes downloaded counter
========================

A shared-object is needed in order to count the downloaded bytes from
the threads. I thought about three ways to achieve it:

1. **A global var**: `shared1`
2. **SharedObject()** (python object with thread locks): `shared2`
3. **multiprocessing.Value**: `shared3`

I've tried their performance, where the read filesize was 67060045
Bytes (Approx. 64MB).
	
========	========	========
shared1		shared2		shared3
========	========	========
67027277	64495949	67010893
67060045	66265421	67043661
67060045	65364301	67060045
67051853	65118541	67043661
67060045	65927843	67060045
67051853	63584931	67043661
67035469	64569677	67051853
========	========	========

The results:

* shared1 has an error rate of **0.07%**.
* shared2 has an error rate of **3.72%**.
* shared3 has an error rate of **0.06%**.


It is not clear why shared2 fails so bad, but we'll stick with shared3 concept for now.