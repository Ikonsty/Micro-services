package com.example.queue;

import com.hazelcast.client.HazelcastClient;
import com.hazelcast.client.config.ClientConfig;
import com.hazelcast.collection.IQueue;
import com.hazelcast.config.Config;
import com.hazelcast.config.QueueConfig;
import com.hazelcast.core.HazelcastInstance;

public class ConsumerBQ {
    public static void start() {
        ClientConfig clientConfig = new ClientConfig();
        clientConfig.setClusterName("dev");

        HazelcastInstance hz = HazelcastClient.newHazelcastClient(clientConfig);
        Config config = new Config();

        QueueConfig queueConfig = config.getQueueConfig("default");
        queueConfig.setName("queue")
                .setMaxSize(10);
        config.addQueueConfig(queueConfig);

        IQueue<Integer> queue = hz.getQueue( "queue" );
        while ( true ) {
            try {
                int item = queue.take();
                System.out.println( "Consumed: " + item );
                if ( item == -1 ) {
                    queue.put( -1 );
                    break;
                }
                Thread.sleep( 500 );
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
        System.out.println( "Consumer Finished!" );
        hz.shutdown();
    }
}
