package com.example.logging;

import java.io.IOException;
import java.util.UUID;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class Message {
    UUID id;
    String txt;

    public Message() {}
    public Message(UUID id, String txt) {
        this.id = id;
        this.txt = txt;
    }
    public Message(String json) throws JsonParseException, JsonMappingException, IOException {
        ObjectMapper mapper = new ObjectMapper();
        Message message = mapper.readValue(json, Message.class);
        this.id = message.getId();
        this.txt = message.getTxt();
    }


    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public String getTxt() {
        return txt;
    }

    public void setTxt(String txt) {
        this.txt = txt;
    }

    @Override
    public String toString() {
        return "Message [id=" + id + ", txt=" + txt + "]";
    }
}
