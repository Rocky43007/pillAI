import React, { useRef, useEffect, useState } from 'react';
import { View, Text, StyleSheet, Button, StatusBar, Pressable } from 'react-native';
import { Camera, useCameraDevice, useCameraPermission } from 'react-native-vision-camera';
import { CameraRoll } from "@react-native-camera-roll/camera-roll";
import axios from 'axios';

const App = () => {
  const camera = useRef(null)
  const { hasPermission, requestPermission } = useCameraPermission()
  const [isPopupVisible, setIsPopupVisible] = useState(false);

  useEffect(() => {
    if (!hasPermission) {
      requestPermission();
    }
  }, []);

  const device = useCameraDevice('back')
  if (device == null) return <NoCameraDeviceError />

  const handlePress = async () => {
    // Take a picture
    const file = await camera.current.takePhoto({
      flash: 'on',
      enableShutterSound: false,
    })

    await CameraRoll.saveAsset(`file://${file.path}`, {
      type: 'photo',
    })

    console.log(`Saved photo at ${file.path}`)

    // Show the popup
    setIsPopupVisible(true);
  };

  const handleBackPress = () => {
    // Hide the popup
    setIsPopupVisible(false);
  };

  return (
    <>
      <StatusBar translucent backgroundColor="rgba(0, 0, 0, 0.26)" />
      {/* Background */}
      <Camera
        ref={camera}
        style={StyleSheet.absoluteFill}
        device={device}
        isActive={true}
        photo={true}
      />

      {/* Foreground */}
      <View className="flex-1 justify-start items-center top-0 pt-7">
        <View className="bg-black/25 w-full grid grid-flow-col p-2">
          <Text className="text-3xl font-bold text-center text-white/90">pillAI</Text>
        </View>
      </View>
      {isPopupVisible && (
        <View style={styles.popup} className="pt-3">
          <View className="pl-[5px]">
            <Pressable onPress={handleBackPress} className="pl-2 bg-gray-600 rounded-full w-[60px]">
              <Text className="text-white text-xl">Back</Text>
            </Pressable>
          </View>
          <View className="pl-[7px]">
            <Text className="text-xl font-bold">Asprin</Text>
            <Text className="text-lg font-extralight">2-Acetoxybenzoic acid</Text>
            <Text className="text-lg font-extralight">C9H8O4</Text>
            <Text className="text-lg">Dosage: 1-2 tablets</Text>
            <Text className="text-md">1-2 tablets</Text>
            <Text className="text-lg">Frequency:</Text>
            <Text className="text-md">Every 4-6 hours</Text>


          </View>
        </View>
      )}
      {!isPopupVisible && (
        <View className="flex-1 justify-end items-center bottom-0 pb-7">
          <Button className="p-2 rounded-3xl bg-gray-300" title="Take Picture" onPress={handlePress} />
        </View>
      )}
    </>
  )
};

const NoCameraDeviceError = () => {
  return (
    <View className="flex-1 justify-center items-center">
      <Text>No camera device found</Text>
    </View>
  )
}

const styles = StyleSheet.create({
  popup: {
    position: 'absolute',
    height: '50%',
    width: '100%',
    bottom: 0,
    backgroundColor: 'white',
    justifyContent: 'start',
    alignItems: 'start',
  },
});

export default App;