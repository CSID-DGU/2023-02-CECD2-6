import yaml
import psycopg2

def get_news_data(target_ids):
    # PostgreSQL 데이터베이스 연결 정보
    with open('../config/DBConfig.yaml', 'r') as yaml_file:
        config_data = yaml.safe_load(yaml_file)

    # PostgreSQL 연결 정보
    db_config = {
        'host': config_data.get('host', 'localhost'),
        'database': config_data.get('database', 'postgres'),
        'user': config_data.get('user', 'postgres'),
        'password': config_data.get('password', ''),
        'port': config_data.get('port', 5432)
    }

    documents = []

    try:
        # PostgreSQL에 연결
        connection = psycopg2.connect(**db_config)

        # 커서 생성
        cursor = connection.cursor()

        # 각 target_id에 대한 데이터 조회 쿼리 실행
        for target_id in target_ids:
            select_data_query = f"SELECT * FROM news WHERE id = {target_id};"
            cursor.execute(select_data_query, (target_id,))

            # 결과 가져오기
            rows = cursor.fetchall()

            # 결과 출력
            for i, row in enumerate(rows):
                article_str = f'{row[5]}'
                article_list = [item.strip() for item in article_str.strip('{}').split(',')]
                documents.append(article_list)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # 연결 및 커서 닫기
        if connection:
            connection.close()
        if cursor:
            cursor.close()

    return documents
