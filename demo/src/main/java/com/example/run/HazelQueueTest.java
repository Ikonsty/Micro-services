package com.example.run;

import com.example.queue.ConsumerBQ;
import com.example.queue.ProducerBQ;

public class HazelQueueTest {
    public static void main(String[] args) {
        Thread thread1 = new Thread(ProducerBQ::start);
        // Thread thread2 = new Thread(ConsumerBQ::start);
        // Thread thread3 = new Thread(ConsumerBQ::start);

        thread1.start();
        // thread2.start();
        // thread3.start();
    }
}
