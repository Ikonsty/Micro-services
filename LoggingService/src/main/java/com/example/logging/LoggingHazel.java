package com.example.logging;

import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Service;

// import com.hazelcast.client.HazelcastClient;
import com.hazelcast.core.Hazelcast;
import com.hazelcast.core.HazelcastInstance;
import java.util.concurrent.ConcurrentMap;
import java.util.*;


@Service
@Primary
public class LoggingHazel implements LoggingService{
    private HazelcastInstance hz = Hazelcast.newHazelcastInstance();
    // private HazelcastInstance hz = HazelcastClient.newHazelcastClient();
    private ConcurrentMap<UUID, String> messages = hz.getMap("my-distributed-map");

    @Override
    public void addToLog(Message msg) {
        messages.put(msg.id, msg.txt);
    }

    @Override
    public Map<UUID, String> log() {return messages; }
}
