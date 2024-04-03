import psycopg2
import unittest
import random
import time

class TestPostgresPerformance(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(
            dbname='ps_db',
            user='admin',
            password='son123aA@',
            host='10.16.150.134',
            port='31879'
        )
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS son_test_table (
                id SERIAL PRIMARY KEY, 
                data VARCHAR
            );
        """)
        self.conn.commit()

    def test_random_read_write_bandwidth(self):
        # Measure bandwidth for random write and read
        start_time = time.time()
        for _ in range(1000):  # Adjust the number of iterations as needed
            random_data = str(random.randint(1, 10000))
            self.cur.execute("INSERT INTO son_test_table (data) VALUES (%s);", (random_data,))
        self.conn.commit()
        write_duration = time.time() - start_time

        start_time = time.time()
        for _ in range(1000):
            self.cur.execute("SELECT data FROM son_test_table ORDER BY RANDOM() LIMIT 1;")
            _ = self.cur.fetchone()
        read_duration = time.time() - start_time

        self.assertTrue(write_duration > 0 and read_duration > 0, "Bandwidth test failed.")
        print(f"Random Write Bandwidth: {1000 / write_duration} ops/sec")
        print(f"Random Read Bandwidth: {1000 / read_duration} ops/sec")

    def test_random_read_write_iops(self):
        # Number of operations to perform for the test
        num_operations = 1000

        # Measure write (insert) IOPS
        write_start_time = time.time()
        for _ in range(num_operations):
            # Insert random data
            data = str(random.randint(1, 10000))
            self.cur.execute("INSERT INTO son_test_table (data) VALUES (%s)", (data,))
        self.conn.commit()
        write_end_time = time.time()
        write_iops = num_operations / (write_end_time - write_start_time)

        # Measure read (select) IOPS
        read_start_time = time.time()
        for _ in range(num_operations):
            # Select random entry
            self.cur.execute("SELECT data FROM son_test_table ORDER BY RANDOM() LIMIT 1")
            _ = self.cur.fetchone()
        read_end_time = time.time()
        read_iops = num_operations / (read_end_time - read_start_time)

        # Assert to ensure that IOPS measurement was successful and log the results
        # This assertion is more for demonstration; in real scenarios, you might want to compare against expected IOPS
        self.assertTrue(write_iops > 0 and read_iops > 0, "IOPS measurement failed.")
        print(f"Random Write IOPS: {write_iops} ops/sec")
        print(f"Random Read IOPS: {read_iops} ops/sec")


    def test_read_write_latency(self):
        # Measure write (insert) latency
        write_start_time = time.time()
        # Insert a unique piece of data to measure write latency accurately
        unique_data = f"latency_test_data_{random.randint(1, 10000)}"
        self.cur.execute("INSERT INTO son_test_table (data) VALUES (%s)", (unique_data,))
        self.conn.commit()
        write_end_time = time.time()
        write_latency = write_end_time - write_start_time

        # Measure read (select) latency
        read_start_time = time.time()
        self.cur.execute("SELECT data FROM son_test_table WHERE data = %s", (unique_data,))
        _ = self.cur.fetchone()
        read_end_time = time.time()
        read_latency = read_end_time - read_start_time

        # Assert to ensure latency was measured and log the results
        self.assertTrue(write_latency > 0 and read_latency > 0, "Latency measurement failed.")
        print(f"Write Latency: {write_latency * 1000} ms")
        print(f"Read Latency: {read_latency * 1000} ms")


    def test_sequential_read_write(self):
        num_entries = 1000  # Number of sequential entries for the test
        write_start_time = time.time()
        for i in range(num_entries):
            # Insert data sequentially
            self.cur.execute("INSERT INTO son_test_table (data) VALUES (%s)", (f"sequential_data_{i}",))
        self.conn.commit()
        write_end_time = time.time()
        
        read_start_time = time.time()
        for i in range(num_entries):
            # Read data sequentially
            self.cur.execute("SELECT data FROM son_test_table WHERE data = %s", (f"sequential_data_{i}",))
            _ = self.cur.fetchone()
        read_end_time = time.time()
        
        print(f"Sequential Write Time: {write_end_time - write_start_time} seconds")
        print(f"Sequential Read Time: {read_end_time - read_start_time} seconds")


    def test_mixed_read_write_iops(self):
        num_operations = 500  # Total number of mixed operations
        mixed_operations_start_time = time.time()
        for i in range(num_operations):
            if i % 2 == 0:  # Alternate between write and read
                # Write operation
                self.cur.execute("INSERT INTO son_test_table (data) VALUES (%s)", (f"mixed_data_{i}",))
            else:
                # Read operation, using a modulo to ensure the index exists
                index_to_read = i % ((i // 2) + 1)
                self.cur.execute("SELECT data FROM son_test_table WHERE data = %s", (f"mixed_data_{index_to_read}",))
                _ = self.cur.fetchone()
        self.conn.commit()
        mixed_operations_end_time = time.time()
        
        total_time = mixed_operations_end_time - mixed_operations_start_time
        iops = num_operations / total_time
        print(f"Mixed Read/Write IOPS: {iops} operations/second")


if __name__ == '__main__':
    unittest.main()
