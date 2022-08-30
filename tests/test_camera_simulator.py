from camera_simulator.processor import Lens, Sensor, lens, SizeImageException
import numpy as np
import pytest

def get_positive_test_data_lens_process():
    size = [(np.random.randint(1,21),np.random.randint(1,21)) for i in range(10)]
    images = [np.random.random(size[i]) for i in range(10)]
    for i in range(10):
        yield size[i][0],size[i][1],images[i]

def get_negative_test_data_incorrect_size_lens_process():
    size = [(np.random.randint(1,20),np.random.randint(1,20)) for i in range(10)]
    images = [np.random.random((np.random.randint(size[i][0]),np.random.randint(size[i][1]))) for i in range(10)]
    for i in range(10):
        yield size[i][0],size[i][1],images[i]


def test_version():
    get_positive_test_data_lens_process()
    assert '0.1.0' == '0.1.0'

@pytest.mark.parametrize("input", get_positive_test_data_lens_process())
def test_lens_process(input):
    lens_pro = Lens(input[0],input[1])
    assert lens_pro.process(input[2]).all() == input[2].all()

@pytest.mark.parametrize("input", get_negative_test_data_incorrect_size_lens_process())
def test_incorrect_size_image(input):
    lens_pro = Lens(input[0],input[1])
    with pytest.raises(SizeImageException) as err:
        lens_pro.process(input[2])
    assert err.type == SizeImageException







