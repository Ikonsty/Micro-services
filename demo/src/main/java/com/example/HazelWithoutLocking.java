package com.example;

import com.hazelcast.client.HazelcastClient;
import com.hazelcast.core.HazelcastInstance;
import java.io.Serializable;
import com.hazelcast.map.IMap;


public class HazelWithoutLocking {
    public static void run() {
        HazelcastInstance hz = HazelcastClient.newHazelcastClient();
        // Різні мапи
        IMap<String, Value> map = hz.getMap( "my-distributed-map-race" );
        String key = "1";
        map.put( key, new Value() );
        System.out.println( "Race starting" );
        for ( int k = 0; k < 1000; k++ ) {
            Value value = map.get( key );
            try {
                Thread.sleep( 10 );
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
            value.amount++;
            map.put( key, value );
        }
        System.out.println( "Race finished! Result = " + map.get(key).amount );
        hz.shutdown();
    }

    static class Value implements Serializable {
        public int amount;
    }
}

// запустити в циклі триччі три треди з різними типами блокування
