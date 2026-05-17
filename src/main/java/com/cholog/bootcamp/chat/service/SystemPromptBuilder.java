package com.cholog.bootcamp.chat.service;

import com.cholog.bootcamp.loader.KnowledgeBase;
import org.springframework.ai.chat.prompt.PromptTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Component;

import java.util.Map;

@Component
public class SystemPromptBuilder {

    private final PromptTemplate template;
    private final KnowledgeBase knowledgeBase;

    public SystemPromptBuilder(
            @Value("classpath:prompts/system.st") Resource templateResource,
            KnowledgeBase knowledgeBase) {
        this.template = new PromptTemplate(templateResource);
        this.knowledgeBase = knowledgeBase;
    }

    public String build() {
        return template.render(Map.of(
                "faq", knowledgeBase.getFaq(),
                "policies", knowledgeBase.getPolicies(),
                "chatLogs", knowledgeBase.getChatLogs()
        ));
    }
}
