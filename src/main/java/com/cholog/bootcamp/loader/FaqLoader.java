package com.cholog.bootcamp.loader;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.nio.file.Paths;

@Component
public class FaqLoader extends MarkdownLoader {

    private final String faqDir;

    public FaqLoader(@Value("${app.data.path:./data}") String dataPath) {
        this.faqDir = Paths.get(dataPath, "layer1_faq").toString();
    }

    public String load() {
        return loadDir(Paths.get(faqDir));
    }
}
