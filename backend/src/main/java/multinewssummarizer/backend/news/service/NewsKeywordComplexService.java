package multinewssummarizer.backend.news.service;

import lombok.RequiredArgsConstructor;
import multinewssummarizer.backend.news.model.NewsKeywordDTO;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class NewsKeywordComplexService {
    private final NewsKeywordService newsKeywordService;
    private final NewsService newsService;

    public List<NewsKeywordDTO> findKeywordsWithinDay() {
        List<Long> newsIds = newsService.getNewsIdsWithinLastDay();
        return newsKeywordService.findNewsKeywordsByNewsIds(newsIds);
    }
}
