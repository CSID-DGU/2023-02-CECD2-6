package multinewssummarizer.backend.news.service;

import lombok.RequiredArgsConstructor;
import multinewssummarizer.backend.news.domain.NewsKeyword;
import multinewssummarizer.backend.news.model.NewsKeywordDTO;
import multinewssummarizer.backend.news.repository.NewsKeywordRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class NewsKeywordService {

    private final NewsKeywordRepository newsKeywordRepository;

    public List<NewsKeyword> findAllByNewsId(Long newsId) {
        return newsKeywordRepository.findAllByNewsId(newsId);
    }

    public List<NewsKeywordDTO> findNewsKeywordsByNewsIds(List<Long> ids) {
        return newsKeywordRepository.findNewsKeywordsByNewsIds(ids);
    }
}
