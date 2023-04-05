package com.example.logging;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;


import org.springframework.http.*;

import java.util.*;

@RestController
public class LoggingController {
    Logger logger = LoggerFactory.getLogger(LoggingController.class);

    private final LoggingService loggingService;

    public LoggingController(LoggingService loggingService) {
        this.loggingService = loggingService;
    }

    @GetMapping("/logging")
    public String listLog() {
        Map<UUID, String> messages = loggingService.log();
        System.out.println("Messages were asked");
        System.out.println(messages.values().toString());
        return messages.values().toString();
    }

    @PostMapping("/logging")
    public ResponseEntity<Void> log(@RequestBody Message msg)  {
        System.out.println(msg);

        loggingService.addToLog(msg);
        return ResponseEntity.ok().build();
    }
}
