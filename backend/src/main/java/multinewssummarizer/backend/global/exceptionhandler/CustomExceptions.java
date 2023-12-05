package multinewssummarizer.backend.global.exceptionhandler;

public class CustomExceptions{

    public static class ExistingIdException extends RuntimeException {
        public ExistingIdException(String message) {
            super(message);
        }
    }

    public static class WrongPasswordException extends RuntimeException {
        public WrongPasswordException(String message) {
            super(message);
        }
    }

    public static class IllegalArgumentLoginException extends RuntimeException {
        public IllegalArgumentLoginException(String message) {
            super(message);
        }
    }

    public static class NoNewsDataException extends RuntimeException {
        public NoNewsDataException(String message) {super(message);}
    }

    public static class NoBatchNewsDataException extends RuntimeException {
        public NoBatchNewsDataException(String message) {super(message);}
    }

    public static class NoSummaryLogException extends RuntimeException {
        public NoSummaryLogException(String message) {super(message);}
    }
}
