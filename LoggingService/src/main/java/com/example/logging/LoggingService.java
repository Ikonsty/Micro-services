package com.example.logging;

import java.util.*;

public interface LoggingService {
    void addToLog(Message msg);

    Map<UUID, String> log();
}
