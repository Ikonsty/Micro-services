package com.example;

import com.hazelcast.client.HazelcastClient;
import com.hazelcast.core.HazelcastInstance;
import java.util.concurrent.ConcurrentMap;

public class HazelOne {
    public static void main(String[] args) {
        // Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
        HazelcastInstance hz = HazelcastClient.newHazelcastClient();
        // Get the Distributed Map from Cluster.
        ConcurrentMap<String, Integer> map = hz.getMap("my-distributed-map");

        for (int i = 0; i < 1000; i++) {
            map.put(String.valueOf(i), i);
        }

        // Shutdown this Hazelcast client
        hz.shutdown();
    }
}