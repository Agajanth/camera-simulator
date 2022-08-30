from camera_simulator.processor import Lens, Sensor, lens, SizeImageException
import numpy as np
import pytest

HEIGHT:int = 4
WIDTH:int = 4
INVALID_HEIGHT:int = -2
INVALID_WIDTH:int = -100
ZERO_HEIGHT:int = 0
ZERO_WIDTH:int =  0
VOID_IMAGE = np.array([[]])
ZERO_GAIN:int = 0
INVALID_GAIN:int = 0
RANDOM_IMAGE = np.random.random((100,100))

def get_data_types():
    data = [True,"Hello_world",RANDOM_IMAGE]
    size = len(data)
    for i in range(size):
        yield data[i],data[size-i-1]

def get_positive_test_data_process():
    size = [(np.random.randint(1,100),np.random.randint(1,100)) for i in range(10)]
    images = [np.random.random(size[i]) for i in range(10)]
    for i in range(10):
        yield size[i][0],size[i][1],images[i]

def get_sensor_data():
    gains = [np.random.random() for i in range(10)]
    for gain in gains:
        if gain < 0:
            yield gain*-1,RANDOM_IMAGE
        else:
            yield gain,RANDOM_IMAGE

def get_negative_test_data_incorrect_size_process():
    size = [(np.random.randint(1,20),np.random.randint(1,20)) for i in range(10)]
    images = [np.random.random((np.random.randint(size[i][0]),np.random.randint(size[i][1]))) for i in range(10)]
    for i in range(10):
        yield size[i][0],size[i][1],images[i]


@pytest.mark.parametrize("input", get_positive_test_data_process())
def test_lens_process_with_positive_test_data(input):
    lens_pro = Lens(input[0],input[1])
    assert lens_pro.process(input[2]).all() == input[2].all()

@pytest.mark.parametrize("input", get_negative_test_data_incorrect_size_process())
def test_incorrect_size_image_lens_process(input):
    lens_pro = Lens(input[0],input[1])
    with pytest.raises(SizeImageException) as err:
        lens_pro.process(input[2])
    assert err.type == SizeImageException

def test_lens_process_with_none_image():
    lens_pro = Lens(HEIGHT,WIDTH)
    with pytest.raises(Exception) as err:
        lens_pro.process(None)
    assert str(err.value) == "image is None"
    assert err.type == Exception

def test_lens_process_with_void_image_and_correct_size():
    lens_pro = Lens(1,ZERO_WIDTH)
    assert lens_pro.process(VOID_IMAGE).all() == VOID_IMAGE.all()

def test_lens_process_with_void_image_and_incorrect_size():
    lens_pro=Lens(ZERO_HEIGHT,ZERO_WIDTH)
    with pytest.raises(SizeImageException) as err:
        lens_pro.process(VOID_IMAGE)
    assert err.type == SizeImageException

@pytest.mark.parametrize("input",get_data_types())
def test_setters_lens(input):
    with pytest.raises(ValueError) as err:
        lens_pro = Lens(input[0],input[1])
    assert err.type == ValueError


@pytest.mark.parametrize("input",get_data_types())
def test_setters_sensor(input) :
    with pytest.raises(ValueError) as err:
        sensor_pro = Sensor(input[0])
    assert err.type == ValueError



@pytest.mark.parametrize("input",get_sensor_data())
def test_process_sensor_with_positive_data(input):
    sensor_pro = Sensor(input[0])
    a =  sensor_pro.process(input[1],100,100,True)
    assert a.all() == (input[0]*input[1]).all()





