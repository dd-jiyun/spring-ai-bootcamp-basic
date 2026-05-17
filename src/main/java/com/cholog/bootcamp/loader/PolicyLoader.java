package com.cholog.bootcamp.loader;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.nio.file.Path;
import java.nio.file.Paths;

// deprecated/ 폴더는 의도적으로 제외 — 구버전 정책이 답변에 섞이는 것을 방지
@Component
public class PolicyLoader extends MarkdownLoader {

    private final Path currentDir;
    private final Path internalDir;

    public PolicyLoader(@Value("${app.data.path:./data}") String dataPath) {
        Path base = Paths.get(dataPath, "layer2_policies");
        this.currentDir = base.resolve("current");
        this.internalDir = base.resolve("internal");
    }

    public String load() {
        return loadDir(currentDir) + loadDir(internalDir);
    }
}
