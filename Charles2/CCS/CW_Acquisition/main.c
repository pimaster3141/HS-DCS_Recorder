#include <msp430.h> 


#define MCLK_XTAL_SRC BIT3
#define SCLK_XTAL_SRC BIT4
#define SCLK_MCU_BYP BIT5
#define QUAD_MCU_SRC BIT6
#define DIS_DETECTORS BIT7
#define DETECTOR_PSU_EN BIT0

#define EN_690 BIT5
#define EN_852 BIT6

void initSystem(void);
void initClk(void);

/**
 * main.c
 */
int main(void)
{
	WDTCTL = WDTPW | WDTHOLD;	// stop watchdog timer
	
	initSystem();
	initClk();

//	P1OUT=0;



	while(1)
	{}

	return 0;
}

void initSystem(void)
{
    P1DIR = 0xFF;   // CLK OUTPUTS
    P2DIR |= BIT0;  // DETECTOR PSU
    P7DIR |= BIT4+BIT5+BIT6;    // LASER INTERLOCKS

    P1OUT = MCLK_XTAL_SRC + SCLK_XTAL_SRC;

    P2OUT = 1;
    P7OUT = 0;

    UCSCTL4 = SELM_3+SELS_3+SELA_3;
    return;
}

void initClk(void)
{


//    P1OUT=0;

    P1SEL |= BIT0;  // SET ACLK OUTPUT
    P5SEL |= BIT2;  // CFG XTAL INPUT
    int i = 0;
    for (i=0; i < 0xFFF; i++)
        __delay_cycles(0xFF);
    UCSCTL6 |= XT2BYPASS;    // ENABLE XTAL2
    for (i=0; i < 0xFFF; i++)
        __delay_cycles(0xFF);
    UCSCTL6 &= ~XT2OFF;
    for (i=0; i < 0xFFF; i++)
        __delay_cycles(0xFF);
    UCSCTL4 = SELA_5 + SELS_5 + SELM_5;   // SET CLKSRC TO XTAL

    while(UCSCTL7 & XT2OFFG)
    {
        UCSCTL4 = SELA_1 + SELS_1 + SELM_1;   // SET CLKSRC TO XTAL
        UCSCTL7 &= ~XT2OFFG;
        for (i=0; i < 0xFF; i++)
            __delay_cycles(0xFF);
        UCSCTL6 = XT2BYPASS;    // ENABLE XTAL2
        for (i=0; i < 0xFF; i++)
            __delay_cycles(0xFF);
        UCSCTL4 = SELA_5 + SELS_5 + SELM_5;   // SET CLKSRC TO XTAL
        for (i=0; i < 0xFF; i++)
            __delay_cycles(0xFF);
    }


    UCSCTL5 |= DIVA_2;  // divide aclk /4
//    UCSCTL5 = DIVA_0;
    P1OUT |= SCLK_MCU_BYP;  // OVERRIDE SYSCLK

}


