################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../makefile.init

RM := cs-rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
ifneq ($(strip $(ASM_DEPS)),)
-include $(ASM_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 
SECONDARY_LIST += \
BBRF103_2.lst \

SECONDARY_SIZE += \
BBRF103_2.siz \


# All Target
all: BBRF103_2.elf secondary-outputs

# Tool invocations
BBRF103_2.elf: $(OBJS) $(USER_OBJS)
	@echo 'Building target: $@'
	@echo 'Invoking: ARM Sourcery Windows GCC C Linker'
	arm-none-eabi-gcc $(OBJS) $(USER_OBJS) $(LIBS) -T"D:\Program Files (x86)\Cypress\EZ-USB FX3 SDK\1.3\/firmware/common/fx3.ld" -nostartfiles -Wl,-Map,BBRF103_2.map -Wl,-d -Wl,--no-wchar-size-warning -Wl,--gc-sections -Wl,--entry,CyU3PFirmwareEntry "D:\Program Files (x86)\Cypress\EZ-USB FX3 SDK\1.3\\firmware\u3p_firmware\lib\fx3_debug\cyfxapi.a" "D:\Program Files (x86)\Cypress\EZ-USB FX3 SDK\1.3\\firmware\u3p_firmware\lib\fx3_debug\cyu3lpp.a" "D:\Program Files (x86)\Cypress\EZ-USB FX3 SDK\1.3\\firmware\u3p_firmware\lib\fx3_debug\cyu3threadx.a" "D:\Program Files (x86)\Cypress\EZ-USB FX3 SDK\1.3\ARM GCC\\arm-none-eabi\lib\libc.a" "D:\Program Files (x86)\Cypress\EZ-USB FX3 SDK\1.3\ARM GCC\\lib\gcc\arm-none-eabi\4.8.1\libgcc.a" -mcpu=arm926ej-s -mthumb-interwork -g -gdwarf-2 -o"BBRF103_2.elf"
	@echo 'Finished building target: $@'
	@echo ' '
	$(MAKE) --no-print-directory post-build

BBRF103_2.lst: BBRF103_2.elf
	@echo 'Invoking: ARM Sourcery Windows GNU Create Listing'
	arm-none-eabi-objdump -h -S BBRF103_2.elf > "BBRF103_2.lst"
	@echo 'Finished building: $@'
	@echo ' '

BBRF103_2.siz: BBRF103_2.elf
	@echo 'Invoking: ARM Sourcery Windows GNU Print Size'
	arm-none-eabi-size  --format=berkeley BBRF103_2.elf
	@echo 'Finished building: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) $(SECONDARY_SIZE)$(OBJS)$(C_DEPS)$(ASM_DEPS)$(EXECUTABLES)$(SECONDARY_LIST)$(S_UPPER_DEPS) BBRF103_2.elf
	-@echo ' '

post-build:
	-@echo 'Converting ELF to image (.img) format'
	-"D:\Program Files (x86)\Cypress\EZ-USB FX3 SDK\1.3\\util\elf2img\elf2img.exe" -i BBRF103_2.elf -o BBRF103_2.img
	-@echo ' '

secondary-outputs: $(SECONDARY_LIST) $(SECONDARY_SIZE)

.PHONY: all clean dependents
.SECONDARY: post-build

-include ../makefile.targets
