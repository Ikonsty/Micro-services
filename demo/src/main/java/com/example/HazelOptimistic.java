package com.example;

import com.hazelcast.client.HazelcastClient;
import com.hazelcast.core.HazelcastInstance;
import java.io.Serializable;
import com.hazelcast.map.IMap;

public class HazelOptimistic {
    public static void optimistic( ) {
        HazelcastInstance hz = HazelcastClient.newHazelcastClient();
        IMap<String, Value> map = hz.getMap( "my-distributed-map-optimistic" );
        String key = "1";
        map.put( key, new Value() );
        System.out.println( "Optimistic starting" );
        for ( int k = 0; k < 1000; k++ ) {
            for (; ; ) {
                Value oldValue = map.get( key );
                Value newValue = new Value( oldValue );
                try {
                    Thread.sleep( 10 );
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
                newValue.amount++;
                if ( map.replace( key, oldValue, newValue ) )
                    break;
            }
        }
        System.out.println( "Optimistic finished! Result = " + map.get( key ).amount );
        hz.shutdown();
    }

    static class Value implements Serializable {
        public int amount;

        public Value() {
        }

        public Value( Value that ) {
            this.amount = that.amount;
        }

        public boolean equals( Object o ) {
            if ( o == this ) return true;
            if ( !( o instanceof Value ) ) return false;
            Value that = ( Value ) o;
            return that.amount == this.amount;
        }
    }
}
