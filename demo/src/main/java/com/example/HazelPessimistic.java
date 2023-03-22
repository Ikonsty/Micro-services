package com.example;

import com.hazelcast.client.HazelcastClient;
import com.hazelcast.core.HazelcastInstance;
import java.io.Serializable;
import com.hazelcast.map.IMap;

public class HazelPessimistic {
    public static void pessimistic() {
        HazelcastInstance hz = HazelcastClient.newHazelcastClient();
        IMap<String, Value> map = hz.getMap( "my-distributed-map-pessimistic" );
        String key = "1";
        map.put( key, new Value() );
        System.out.println( "Pessimistic starting" );
        for ( int k = 0; k < 1000; k++ ) {
            map.lock( key );
            try {
                Value value = map.get( key );
                try {
                    Thread.sleep( 10 );
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
                value.amount++;
                map.put( key, value );
            } finally {
                map.unlock( key );
            }
        }
        System.out.println( "Pessimistic finished! Result = " + map.get( key ).amount );
        hz.shutdown();
    }

    static class Value implements Serializable {
        public int amount;
    }
}
