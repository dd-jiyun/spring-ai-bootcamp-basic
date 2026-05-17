package com.cholog.bootcamp.loader;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.Stream;

@Component
public class ChatLogLoader {

    private final Path chatlogDir;
    private final ObjectMapper objectMapper = new ObjectMapper();

    public ChatLogLoader(@Value("${app.data.path:./data}") String dataPath) {
        this.chatlogDir = Paths.get(dataPath, "layer3_chatlogs");
    }

    public String load() {
        StringBuilder sb = new StringBuilder();
        try (Stream<Path> files = Files.list(chatlogDir)) {
            files.filter(p -> p.toString().endsWith(".jsonl"))
                    .sorted()
                    .forEach(file -> parseFile(file, sb));
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        return sb.toString();
    }

    private void parseFile(Path file, StringBuilder sb) {
        try {
            for (String line : Files.readAllLines(file)) {
                if (line.isBlank()) continue;
                JsonNode root = objectMapper.readTree(line);

                if (!"correct".equals(root.path("agent_accuracy").asText())) continue;

                JsonNode turns = root.path("turns");
                if (!turns.isArray()) continue;

                sb.append("[대화 예시]\n");
                for (JsonNode turn : turns) {
                    String role = turn.path("role").asText();
                    String text = turn.path("text").asText();
                    String label = "customer".equals(role) ? "고객" : "상담사";
                    sb.append(label).append(": ").append(text).append("\n");
                }
                sb.append("\n");
            }
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }
}
