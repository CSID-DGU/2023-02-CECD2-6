import yaml
import psycopg2
from sshtunnel import SSHTunnelForwarder

def get_news_data(target_ids):
    # PostgreSQL 데이터베이스 연결 정보
    with open('../config/DBConfig.yaml', 'r') as yaml_file:
        config_data = yaml.safe_load(yaml_file)

    print(config_data)
    print(config_data.get('DB_HOST', 'localhost'))
    # PostgreSQL 연결 정보
    ssh_config = {
        'SSH_HOST': config_data.get('SSH_HOST', '3.34.253.81'),
        'SSH_PORT': config_data.get('SSH_PORT', 22),
        'SSH_USERNAME': config_data.get('SSH_USERNAME', 'ubuntu'),
        'SSH_PRIVATE_KEY': config_data.get('SSH_PRIVATE_KEY', 'C:/Users/son/.ssh/gds2023.pem'),
    }
    db_config = {
        'host': config_data.get('DB_HOST', 'localhost'),
        'database': config_data.get('DB_NAME', 'postgres'),
        'user': config_data.get('DB_USER', 'postgres'),
        'password': config_data.get('DB_PASSWORD', ''),
        'port': config_data.get('DB_PORT', 5432)
    }
    print(db_config)
    documents = []

    try:
        # PostgreSQL에 연결
        #connection = psycopg2.connect(**db_config)
        connection, tunnel = create_db_connection(ssh_config,db_config)

        # 커서 생성
        cursor = connection.cursor()

        # 각 target_id에 대한 데이터 조회 쿼리 실행
        for target_id in target_ids:
            select_data_query = f"SELECT * FROM news WHERE id = {target_id};"
            cursor.execute(select_data_query, (target_id,))
            
            #cursor.execute("SELECT COUNT(*) FROM news")
            #count = cursor.fetchone()[0]

            # 결과 가져오기
            rows = cursor.fetchall()

            # 결과 출력
            for i, row in enumerate(rows):
                article_str = f'{row[5]}'
                article_list = [item.strip() for item in article_str.strip('{}').split(',')]
                documents.append(article_list)
        
        print(documents)
        
        # 연결 및 커서 닫기
        if connection:
            close_db_connection(connection, tunnel)
            #connection.close()
        if cursor:
            cursor.close()

        return documents

    except Exception as e:
        print(f"Error: {e}")

# SSH 터널을 통해 데이터베이스 연결을 설정하는 함수
def create_db_connection(ssh_config,db_config):
    tunnel = SSHTunnelForwarder(
        (ssh_config['SSH_HOST'], ssh_config['SSH_PORT']),
        ssh_username=ssh_config['SSH_USERNAME'],
        ssh_pkey=ssh_config['SSH_PRIVATE_KEY'],
        remote_bind_address=(db_config['host'], db_config['port'])
    )
    tunnel.start()

    #connection = psycopg2.connect(**db_config)
    connection = psycopg2.connect(
        host='127.0.0.1',  # 터널을 통해 연결
        port=tunnel.local_bind_port,
        user=db_config['user'],
        password=db_config['password'],
        dbname=db_config['database']
    )
    return connection, tunnel

# 데이터베이스 연결을 닫는 함수
def close_db_connection(conn, tunnel):
    conn.close()
    tunnel.stop()