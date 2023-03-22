package com.example.queue;

import com.hazelcast.client.HazelcastClient;
import com.hazelcast.client.config.ClientConfig;
import com.hazelcast.collection.IQueue;
import com.hazelcast.config.Config;
import com.hazelcast.config.QueueConfig;
import com.hazelcast.core.HazelcastInstance;


public class ProducerBQ {
    public static void start() {
        ClientConfig clientConfig = new ClientConfig();
        clientConfig.setClusterName("dev");

        HazelcastInstance hz = HazelcastClient.newHazelcastClient();
        Config config = new Config();

        QueueConfig queueConfig = config.getQueueConfig("default");
        queueConfig.setName("queue")
                .setMaxSize(10);
        config.addQueueConfig(queueConfig);

        IQueue<Integer> queue = hz.getQueue( "queue" );
        for ( int k = 1; k < 100; k++ ) {
            try {
                queue.put( k );
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
            System.out.println( "Producing: " + k );
            try {
                Thread.sleep( 10 );
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
        try {
            queue.put( -1 );
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
        System.out.println( "Producer Finished!" );
        hz.shutdown();
    }
}
