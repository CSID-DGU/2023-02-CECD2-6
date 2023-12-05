package multinewssummarizer.backend.news.service;

import lombok.RequiredArgsConstructor;
import multinewssummarizer.backend.news.repository.NewsRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class NewsService {
    private final NewsRepository newsRepository;

    public List<Long> getNewsIdsWithinLastDay() {
        return newsRepository.findNewsByPublishedWithinLastDay();
    }
}
