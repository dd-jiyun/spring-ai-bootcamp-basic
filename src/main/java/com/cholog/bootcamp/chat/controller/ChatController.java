package com.cholog.bootcamp.chat.controller;

import com.cholog.bootcamp.chat.dto.ChatRequest;
import com.cholog.bootcamp.chat.dto.ChatResponse;
import com.cholog.bootcamp.chat.service.ChatService;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class ChatController {

    private final ChatService chatService;

    public ChatController(ChatService chatService) {
        this.chatService = chatService;
    }

    @PostMapping("/chat")
    public ChatResponse chat(@RequestBody ChatRequest request) {
        return chatService.ask(request.question());
    }
}
