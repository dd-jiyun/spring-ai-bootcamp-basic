package com.cholog.bootcamp.chat.dto;

public record ChatResponse(
        String answer,
        TokenUsage tokenUsage
) {
}
