package com.cholog.bootcamp.loader;

import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component
public class KnowledgeBase {

    private static final Logger log = LoggerFactory.getLogger(KnowledgeBase.class);

    private final FaqLoader faqLoader;
    private final PolicyLoader policyLoader;
    private final ChatLogLoader chatLogLoader;

    private String faq;
    private String policies;
    private String chatLogs;

    public KnowledgeBase(FaqLoader faqLoader, PolicyLoader policyLoader, ChatLogLoader chatLogLoader) {
        this.faqLoader = faqLoader;
        this.policyLoader = policyLoader;
        this.chatLogLoader = chatLogLoader;
    }

    @PostConstruct
    void load() {
        this.faq = faqLoader.load();
        this.policies = policyLoader.load();
        this.chatLogs = chatLogLoader.load();

        log.info("KnowledgeBase loaded — faq: {}chars, policies: {}chars, chatLogs: {}chars",
                faq.length(), policies.length(), chatLogs.length());
    }

    public String getFaq() { return faq; }
    public String getPolicies() { return policies; }
    public String getChatLogs() { return chatLogs; }
}
