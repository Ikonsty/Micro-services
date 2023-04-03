import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.*;

import java.util.*;

@SpringBootApplication
@RestController
public class LoggingService {

    private Map<String, String> messages = new HashMap<>();

    @GetMapping("/logging")
    public ResponseEntity<String> getAllMessages() {
        String all = "";
        for (String uuid : messages.keySet()) {
            all += messages.get(uuid) + "; ";
        }
        System.out.println("\tLOGGING-LOGS: Send messages");
        return ResponseEntity.ok().body(all.substring(0, all.length() - 2));
    }

    @PostMapping("/logging")
    public ResponseEntity<Map<String, String>> addMessage(@RequestBody Map<String, String> message) {
        String uuid = message.get("uuid");
        String msg = message.get("msg");

        if (uuid == null || msg == null) {
            return ResponseEntity.badRequest().build();
        }

        messages.put(uuid, msg);
        System.out.printf("\tLOGGING-LOGS: New message is %s\nUuid is: %s\n", msg, uuid);
        return ResponseEntity.status(HttpStatus.CREATED).body(message);
    }

    public static void main(String[] args) {
        SpringApplication.run(LoggingService.class, args);
    }
}
