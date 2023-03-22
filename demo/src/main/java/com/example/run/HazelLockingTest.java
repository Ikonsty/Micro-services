package com.example.run;

import com.example.HazelOptimistic;
import com.example.HazelPessimistic;
import com.example.HazelWithoutLocking;

public class HazelLockingTest {
    public static void main(String[] args) {
        for(int i = 0; i < 3; i++) {
            Thread thread1 = new Thread(HazelWithoutLocking::run);
            Thread thread2 = new Thread(HazelPessimistic::pessimistic);
            Thread thread3 = new Thread(HazelOptimistic::optimistic);

            thread1.start();
            thread2.start();
            thread3.start();
        }
    }
}
