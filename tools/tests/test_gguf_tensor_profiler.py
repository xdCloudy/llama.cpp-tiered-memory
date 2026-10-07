import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gguf_tensor_profiler as profiler
from gguf import GGUFWriter


class EntropyTests(unittest.TestCase):
    def test_empty_and_constant_histograms(self):
        self.assertEqual(profiler.shannon_entropy(np.zeros(256, dtype=np.uint64), 0), 0.0)
        hist = np.zeros(256, dtype=np.uint64)
        hist[42] = 100
        self.assertEqual(profiler.shannon_entropy(hist, 100), 0.0)

    def test_uniform_two_symbols_has_one_bit_entropy(self):
        hist = np.zeros(256, dtype=np.uint64)
        hist[0] = hist[1] = 5
        self.assertAlmostEqual(profiler.shannon_entropy(hist, 10), 1.0)


class SamplingTests(unittest.TestCase):
    def test_full_scan_yields_all_bytes_in_order(self):
        data = np.arange(31, dtype=np.uint8)
        chunks = list(profiler.iter_sampled_chunks(data, 0, 7))
        self.assertEqual(b"".join(chunks), data.tobytes())

    def test_sample_is_bounded_and_spread_across_tensor(self):
        data = np.arange(10000, dtype=np.uint32).view(np.uint8)
        chunks = list(profiler.iter_sampled_chunks(data, 1000, 100))
        self.assertLessEqual(sum(map(len, chunks)), 1000)
        joined = b"".join(chunks)
        self.assertGreater(len(joined), 0)
        self.assertLess(joined[0], 255)
        self.assertNotEqual(joined[:100], joined[-100:])

    def test_invalid_chunk_size_is_rejected(self):
        with self.assertRaises(ValueError):
            list(profiler.iter_sampled_chunks(np.zeros(4, dtype=np.uint8), 0, 0))


class ClassificationTests(unittest.TestCase):
    def test_layer_and_expert_tensor_role(self):
        role, layer, expert_id = profiler.classify_tensor("blk.12.ffn_up_exps.weight")
        self.assertEqual((role, layer, expert_id), ("expert_weight", 12, "embedded"))

    def test_explicit_expert_id(self):
        role, layer, expert_id = profiler.classify_tensor("blk.3.expert.7.ffn_up.weight")
        self.assertEqual((role, layer, expert_id), ("expert_weight", 3, 7))


class CodecTests(unittest.TestCase):
    def test_zstd_round_trip_and_accounting(self):
        raw = (b"packed-weights-" * 1000) + bytes(range(256))
        result = profiler.measure_codec([raw[:4096], raw[4096:]], "zstd", 1)
        self.assertEqual(result["round_trip"], "exact")
        self.assertEqual(result["input_bytes"], len(raw))
        self.assertEqual(result["saving_bytes"], len(raw) - result["compressed_bytes"])
        self.assertGreater(result["decode_mib_s"], 0)

    def test_lz4_round_trip_when_installed(self):
        try:
            import lz4.frame  # noqa: F401
        except ImportError:
            self.skipTest("optional lz4 package is not installed")
        raw = bytes(range(256)) * 32
        result = profiler.measure_codec([raw], "lz4", None)
        self.assertEqual(result["round_trip"], "exact")
        self.assertEqual(result["input_bytes"], len(raw))


class GGUFIntegrationTests(unittest.TestCase):
    def test_profiles_generated_gguf_tensor(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "fixture.gguf"
            writer = GGUFWriter(path, "llama")
            writer.add_tensor("blk.0.ffn_up.weight", np.arange(64, dtype=np.float32))
            writer.write_header_to_file()
            writer.write_kv_data_to_file()
            writer.write_tensors_to_file()
            writer.close()

            report = profiler.profile_file(path, [64], 0, ["zstd"], [1])
            self.assertIn("tool_commit", report["environment"])
            self.assertEqual(len(report["environment"]["tool_sha256"]), 64)
            self.assertIn("zstd", report["environment"]["codec_versions"])
            tensor = report["tensors"][0]
            measurement = tensor["measurements"][0]
            self.assertEqual(tensor["type"], "F32")
            self.assertEqual(tensor["logical_bytes"], 64 * 4)
            self.assertEqual(tensor["role"], "feed_forward")
            self.assertEqual(measurement["sample_mode"], "full")
            self.assertEqual(measurement["round_trip"], "exact")
            self.assertIn("estimated_pcie_bytes_saved_per_tensor", measurement)
if __name__ == "__main__":
    unittest.main()
