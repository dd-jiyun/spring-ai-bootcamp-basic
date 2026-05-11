package com.cholog.bootcamp.chat.dto;

public record TokenUsage(
        int promptTokens,
        int completionTokens,
        int totalTokens
) {
}
