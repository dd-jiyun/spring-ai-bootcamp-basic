package com.cholog.bootcamp.chat.service;

import com.cholog.bootcamp.chat.dto.ChatResponse;
import com.cholog.bootcamp.chat.dto.TokenUsage;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.metadata.Usage;
import org.springframework.stereotype.Service;

import java.util.Objects;

@Service
public class ChatService {

    private final ChatClient chatClient;
    private final SystemPromptBuilder systemPromptBuilder;

    public ChatService(ChatClient.Builder builder, SystemPromptBuilder systemPromptBuilder) {
        this.chatClient = builder.build();
        this.systemPromptBuilder = systemPromptBuilder;
    }

    public ChatResponse ask(String question) {
        org.springframework.ai.chat.model.ChatResponse response = chatClient.prompt()
                .system(systemPromptBuilder.build())
                .user(question)
                .call()
                .chatResponse();

        String answer = Objects.requireNonNull(response).getResult().getOutput().getText();
        Usage usage = response.getMetadata().getUsage();

        return new ChatResponse(
                answer,
                new TokenUsage(
                        usage.getPromptTokens(),
                        usage.getCompletionTokens(),
                        usage.getTotalTokens()
                )
        );
    }
}
