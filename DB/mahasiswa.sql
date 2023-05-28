SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_kampus`
--

-- --------------------------------------------------------

--
-- Table structure for table `mahasiswa`
--

CREATE TABLE `mahasiswa` (
  `id_mahasiswa` int(11) NOT NULL AUTO_INCREMENT,
  `nim` varchar(10) NOT NULL,
  `nama_mahasiswa` varchar(100) NOT NULL,
  `fakultas` varchar(20) DEFAULT NULL,
  `prodi` varchar(20) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `alamat` varchar(100) NOT NULL,
  PRIMARY KEY (`id_mahasiswa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `mahasiswa`
--

INSERT INTO `mahasiswa` (`nim`, `nama_mahasiswa`, `fakultas`, `prodi`, `phone`, `email`, `alamat`) VALUES
('44368734', 'FIKRI HADI NUGRAHA', 'Sains dan Teknologi', 'Sistem Informasi', '8121842', '', ''),
('10122126', 'FIKRI HADI NUGRAHA', 'TEKNIK', 'Sistem Informasi', '08121845', 'fikar123@gmail.com', 'ali@123.com'),
('10122126', 'BETRIS KUMALASARI', 'Sains Teknologi', 'TEKNIK ELECTRO', '081218427611', 'CIKANDE', 'sigit@gmail.com');

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `mahasiswa`
--
ALTER TABLE `mahasiswa` AUTO_INCREMENT = 4;

--
-- Create stored procedure to update AUTO_INCREMENT value after delete
--
DELIMITER //
CREATE PROCEDURE update_auto_increment()
BEGIN
    DECLARE max_id INT;
    SET max_id = (SELECT MAX(id_mahasiswa) FROM mahasiswa);
    IF max_id IS NULL THEN
        SET max_id = 0;
    END IF;
    SET @max_id_sql = CONCAT('ALTER TABLE mahasiswa AUTO_INCREMENT = ', max_id + 1);
    PREPARE stmt FROM @max_id_sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

--
-- Create trigger to call the stored procedure after delete
DELIMITER //
CREATE TRIGGER trg_before_delete_mahasiswa AFTER DELETE ON mahasiswa
FOR EACH ROW
BEGIN
    CALL update_auto_increment();
END //
DELIMITER ;



/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

COMMIT;
