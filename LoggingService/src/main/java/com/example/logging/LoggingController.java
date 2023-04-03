package com.example.logging;

import org.apache.logging.log4j.message.Message;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.*;

import java.util.*;
// 6
// 5
// -
// _
// +
// =

public class LoggingController {
    Logger logger = LoggerFactory.getLogger(LoggingController.class);

    private final LoggingService loggingService;

    public LoggingController(LoggingService loggingService) {
        this.loggingService = loggingService;
    }

    @GetMapping("/log")
    public String listLog() {
        Map<UUID, String> messages = loggingService.log();
        return messages.values().toString();
    }

    @PostMapping("/log")
    public ResponseEntity<Void> log(@RequestBody Message msg) {
        logger.info(msg.toString());
        loggingService.addToLog(msg);
        return ResponseEntity.ok().build();
    }
}
