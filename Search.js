import React, { useRef, useEffect } from 'react';
import { View, Text, StyleSheet, Button, StatusBar } from 'react-native';
import { Camera, useCameraDevice, useCameraPermission } from 'react-native-vision-camera';
import { CameraRoll } from "@react-native-camera-roll/camera-roll";
import axios from 'axios';

const App = () => {
  const { hasPermission, requestPermission } = useCameraPermission()

  useEffect(() => {
    if (!hasPermission) {
      requestPermission();
    }
  }, []);

  /** @type {React.MutableRefObject<import('react-native-vision-camera').Camera>} */
  const camera = useRef(null)

  const device = useCameraDevice('back')
  if (device == null) return <NoCameraDeviceError />

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
      <View className="flex-1 justify-end items-center bottom-0 pb-7">
        <Button className="p-2 rounded-3xl bg-gray-300" title="Take Picture" onPress={async () => {
          // Take a picture
          const file = await camera.current.takePhoto({
            flash: 'on',
            enableShutterSound: false,
          })

          await CameraRoll.saveAsset(`file://${file.path}`, {
            type: 'photo',
          })

          console.log(`Saved photo at ${file.path}`)
        }}/>
      </View>
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

export default App;
