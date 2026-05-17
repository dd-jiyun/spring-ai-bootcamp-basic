package com.cholog.bootcamp.loader;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.function.Predicate;
import java.util.stream.Stream;

public abstract class MarkdownLoader {

    protected String loadDir(Path dir) {
        return loadDir(dir, p -> true);
    }

    protected String loadDir(Path dir, Predicate<Path> filter) {
        StringBuilder sb = new StringBuilder();
        try (Stream<Path> files = Files.list(dir)) {
            files.filter(p -> p.toString().endsWith(".md"))
                    .filter(filter)
                    .sorted()
                    .forEach(file -> {
                        try {
                            sb.append("### ").append(file.getFileName()).append("\n");
                            sb.append(Files.readString(file)).append("\n\n");
                        } catch (IOException e) {
                            throw new UncheckedIOException(e);
                        }
                    });
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        return sb.toString();
    }
}
