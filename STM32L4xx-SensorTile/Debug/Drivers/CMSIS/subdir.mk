################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Projects/Multi/Applications/ALLMEMS1/Src/system_stm32l4xx.c 

OBJS += \
./Drivers/CMSIS/system_stm32l4xx.o 

C_DEPS += \
./Drivers/CMSIS/system_stm32l4xx.d 


# Each subdirectory must supply rules for building sources it contributes
Drivers/CMSIS/system_stm32l4xx.o: C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Projects/Multi/Applications/ALLMEMS1/Src/system_stm32l4xx.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU GCC Compiler'
	@echo $(PWD)
	arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16 -std=c99 -DUSE_HAL_DRIVER -DSTM32_SENSORTILE -DSTM32L476xx -DUSE_STM32L4XX_NUCLEO -DALLMEMS1 -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Projects/Multi/Applications/ALLMEMS1/Inc" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Drivers/CMSIS/Device/ST/STM32L4xx/Include" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Drivers/STM32L4xx_HAL_Driver/Inc" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Drivers/BSP/SensorTile" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Drivers/CMSIS/Include" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Drivers/BSP/Components/Common" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Middlewares/ST/STM32_BlueNRG/SimpleBlueNRG_HCI/includes" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Middlewares/ST/STM32_BlueNRG/Interface" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Drivers/BSP/Components/lsm6dsm" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Drivers/BSP/Components/hts221" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Drivers/BSP/Components/lps22hb" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Drivers/BSP/Components/lsm303agr" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Drivers/BSP/Components/stc3115" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Middlewares/ST/STM32_MotionAR_Library/Inc" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Middlewares/ST/STM32_MotionCP_Library/Inc" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Middlewares/ST/STM32_MotionFX_Library/Inc" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Middlewares/ST/STM32_MotionGR_Library/Inc" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Middlewares/ST/STM32_BlueVoiceADPCM_Library/Inc" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Middlewares/ST/STM32_MetaDataManager" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Middlewares/ST/STM32_USB_Device_Library/Class/CDC/Inc" -I"C:/STM32CubeFunctionPack_ALLMEMS1_V3.1.0/Middlewares/ST/STM32_USB_Device_Library/Core/Inc"  -Os -g3 -Wall -fmessage-length=0 -ffunction-sections -c -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


